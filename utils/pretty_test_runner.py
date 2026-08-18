from functools import wraps
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import sys
import time


def truncate_param(arg, max_str=100, max_seq=10):
    if isinstance(arg, str):
        return arg if len(arg) <= max_str else arg[:max_str] + "..."
    elif isinstance(arg, (list, tuple, set)):
        truncated_seq = [
            truncate_param(item, max_str, max_seq) for item in list(arg)[:max_seq]
        ]
        if len(arg) > max_seq:
            truncated_seq.append(f"... (+{len(arg) - max_seq} more)")
        return truncated_seq if not isinstance(arg, tuple) else tuple(truncated_seq)
    elif isinstance(arg, dict):
        truncated_dict = {
            k: truncate_param(v, max_str, max_seq)
            for i, (k, v) in enumerate(arg.items())
            if i < max_seq
        }
        if len(arg) > max_seq:
            truncated_dict["..."] = f"(+{len(arg) - max_seq} keys)"
        return truncated_dict
    return arg


def pretty_test_runner(time_limit_in_sec=None, stop_on_tc_failure=False):
    """
    Decorator for test functions that formats output, handles timeouts, and optionally
    halts execution on failure.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Print [RUN] <args>
            fmt_args = [truncate_param(a) for a in args]
            fmt_kwargs = {k: truncate_param(v) for k, v in kwargs.items()}
            args_str = ", ".join(map(str, fmt_args))
            kwargs_str = ", ".join(f"{k}={v}" for k, v in fmt_kwargs.items())
            all_args_str = ", ".join(filter(None, [args_str, kwargs_str]))
            print(f"[RUN] {func.__name__}({all_args_str})")

            passed = False
            error_msg = None
            timed_out = False

            start_time = time.perf_counter()

            if time_limit_in_sec is not None and time_limit_in_sec > 0:
                # Execute test function with a timeout using ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(func, *args, **kwargs)
                    try:
                        result = future.result(timeout=time_limit_in_sec)
                        # Expecting function return: (bool_status, str_error_msg)
                        if isinstance(result, tuple) and len(result) == 2:
                            passed, error_msg = result
                        else:
                            passed = bool(result)
                            error_msg = "Test returned unexpected format (expected tuple: (bool, str))."
                    except TimeoutError:
                        timed_out = True
                        passed = False
                        error_msg = f"Test timed out after {time_limit_in_sec} seconds."
                    except Exception as e:
                        passed = False
                        error_msg = f"Test raised an unhandled exception: {str(e)}"
                        raise e
            else:
                # Run standard execution without time limit
                try:
                    result = func(*args, **kwargs)
                    if isinstance(result, tuple) and len(result) == 2:
                        passed, error_msg = result
                    else:
                        passed = bool(result)
                        error_msg = "Test returned unexpected format (expected tuple: (bool, str))."
                except Exception as e:
                    passed = False
                    error_msg = f"Test raised an unhandled exception: {str(e)}"

            duration = time.perf_counter() - start_time

            # Format and print results according to rules
            if passed:
                print(f"[DONE] ({duration:.6f}s)")
            else:
                if error_msg:
                    print(f"Error: {error_msg}")
                print(f"[FAILED] ({duration:.6f}s)")

                if stop_on_tc_failure:
                    print(
                        "Stopping execution due to test failure (stop_on_tc_failure=True)."
                    )
                    sys.exit(1)

            return passed, error_msg

        return wrapper

    # Allow decorator to be used either with or without parentheses: @PrettyTestRun or @PrettyTestRun(...)
    if callable(time_limit_in_sec):
        func = time_limit_in_sec
        time_limit_in_sec = None
        return decorator(func)

    return decorator
