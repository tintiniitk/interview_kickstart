# This script is not for executing, but rather for sourcing from other commands.
# This contains useful functions and config variables.

# localhost config
LOCALHOST=http://127.0.0.1:8000

# Define the runner function
function run_and_log() {
    # Store the first argument as the command string
    local cmd="$1"

    # Print the command (using a prefix for clarity)
    echo "Executing: $cmd"

    # Execute the string and let it evaluate bash syntax naturally
    eval "$cmd"

    # Capture and return the exit code of the eval statement
    return $?
}

function start_fast_api_web_server_on_localhost() {
    uvicorn main:app --reload
}