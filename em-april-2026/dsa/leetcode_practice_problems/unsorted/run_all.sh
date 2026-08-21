#!/bin/bash

# ==============================================================================
# CONFIGURATION
# ==============================================================================
# List of directory names to skip entirely
DISALLOW_LIST=("03630_Partition_Array_for_Maximum_XOR_and_AND" "00037_sudoku_solver")

# Max parallel jobs (defaults to number of CPU cores, fallback to 4)
MAX_JOBS=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

# Log file timestamp identifier
RUN_TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILENAME="run-${RUN_TIMESTAMP}.log"

# Temporary file for thread-safe summary aggregation
SUMMARY_FILE=$(mktemp)

# ==============================================================================
# INITIALIZATION & HEADER
# ==============================================================================
echo "Starting test suite in parallel using up to $MAX_JOBS worker processes..."
echo ""
printf "%-22s | %-8s | %-10s | %-10s | %-20s\n" "Subdirectory" "Status" "Start Time" "End Time" "Reason / Log"
printf "%.s-" {1..80}
printf "\n"

# ==============================================================================
# PARALLEL EXECUTION ENGINE
# ==============================================================================
find . -mindepth 1 -maxdepth 1 -type d -exec test -e "{}/Makefile" \; -print0 | while IFS= read -r -d '' dir; do

    # Throttle concurrency: Wait if active background jobs reach MAX_JOBS limit
    while [ $(jobs -r | wc -l) -ge $MAX_JOBS ]; do
        sleep 0.1
    done

    # Dispatch directory execution to a background subshell
    (
        dir_name=$(basename "$dir")
        log_file_path="${dir}/${LOG_FILENAME}"

        start_time=$(date +"%H:%M:%S")
        status="PASSED"
        reason="Success"

        # ----------------------------------------------------------------------
        # 1. DISALLOW LIST CHECK
        # ----------------------------------------------------------------------
        if [[ " ${DISALLOW_LIST[*]} " =~ " ${dir_name} " ]]; then
            status="IGNORED"
            reason="In disallow_list"
            end_time=$(date +"%H:%M:%S")

            # Print real-time thread-safe output to stdout (Yellow for IGNORED)
            printf "%-22s | \033[0;33m%-8s\033[0m | %-10s | %-10s | %-20s\n" \
                   "$dir_name" "$status" "$start_time" "$end_time" "$reason"

            # Record atomic entry to summary
            echo "$dir_name|$status|$start_time|$end_time|$reason" >> "$SUMMARY_FILE"
            exit 0
        fi

        # ----------------------------------------------------------------------
        # 2. RUN BUILD AND MAIN WITH TIMEOUT
        # ----------------------------------------------------------------------
        (
            cd "$dir" || exit 1

            {
                echo "=== TEST START: $(date) ==="
                echo "--- Executing: make ---"

                # Step A: Run make
                make 2>&1
                make_status=$?

                if [ $make_status -ne 0 ]; then
                    echo "=== MAKE FAILED with exit code $make_status ==="
                    exit 101
                fi

                echo "--- Executing: timeout 60s ./main ---"
                # Step B: Run ./main with a 60s timeout
                timeout 60s ./main 2>&1
                main_status=$?

                if [ $main_status -eq 124 ]; then
                    echo "=== MAIN TIMED OUT (Exceeded 60s) ==="
                    exit 102
                elif [ $main_status -ne 0 ]; then
                    echo "=== MAIN FAILED with exit code $main_status ==="
                    exit 103
                fi

            } > "$LOG_FILENAME" 2>&1

            exec_status=$?

            # Step C: Log file inspection for 'error' or 'fail'
            if grep -iqE "error|fail" "$LOG_FILENAME"; then
                if [ $exec_status -eq 0 ]; then
                    exit 104 # Error/fail string found in logs despite 0 exit code
                fi
            fi

            exit $exec_status
        )

        subshell_status=$?
        end_time=$(date +"%H:%M:%S")

        # ----------------------------------------------------------------------
        # 3. FAILURE CATEGORIZATION
        # ----------------------------------------------------------------------
        if [ $subshell_status -ne 0 ]; then
            status="FAILED"
            case $subshell_status in
                101) reason="Make error" ;;
                102) reason="Timed out (>60s)" ;;
                103) reason="Main exit code non-zero" ;;
                104) reason="Found 'error'/'fail' in log" ;;
                *)   reason="Error code ($subshell_status)" ;;
            esac
        fi

        # ----------------------------------------------------------------------
        # 4. REAL-TIME CONSOLE OUTPUT
        # ----------------------------------------------------------------------
        if [ "$status" = "PASSED" ]; then
            printf "%-22s | \033[0;32m%-8s\033[0m | %-10s | %-10s | %-20s\n" \
                   "$dir_name" "$status" "$start_time" "$end_time" "$LOG_FILENAME"
        else
            printf "%-22s | \033[0;31m%-8s\033[0m | %-10s | %-10s | %-20s\n" \
                   "$dir_name" "$status" "$start_time" "$end_time" "$reason"
        fi

        # Record atomic line to summary file
        echo "$dir_name|$status|$start_time|$end_time|$reason" >> "$SUMMARY_FILE"

    ) &

done

# Block execution until all background workers have finished
wait

function generate_consolidated_summary_report()
{
    # ==============================================================================
    # CONSOLIDATED SUMMARY REPORT
    # ==============================================================================
    printf "%.s=" {1..80}
    printf "\n"
    echo "                      CONSOLIDATED REPORT SUMMARY"
    printf "%.s=" {1..80}
    printf "\n"
    printf "%-22s | %-8s | %-10s | %-10s | %-20s\n" "Subdirectory" "Status" "Start Time" "End Time" "Notes / Reason"
    printf "%.s-" {1..80}
    printf "\n"

    # Render summary table rows from stored entries
    while IFS='|' read -r s_dir s_status s_start s_end s_reason; do
        if [ "$s_status" = "PASSED" ]; then
            printf "%-22s | \033[0;32m%-8s\033[0m | %-10s | %-10s | %-20s\n" \
                   "$s_dir" "$s_status" "$s_start" "$s_end" "Success"
        elif [ "$s_status" = "IGNORED" ]; then
            printf "%-22s | \033[0;33m%-8s\033[0m | %-10s | %-10s | %-20s\n" \
                   "$s_dir" "$s_status" "$s_start" "$s_end" "$s_reason"
        else
            printf "%-22s | \033[0;31m%-8s\033[0m | %-10s | %-10s | %-20s\n" \
                   "$s_dir" "$s_status" "$s_start" "$s_end" "$s_reason"
        fi
    done < "$SUMMARY_FILE"

    printf "%.s=" {1..80}
    printf "\n\n"
}

# generate_consolidated_summary_report()

# Clean up temp file
rm -f "$SUMMARY_FILE"
