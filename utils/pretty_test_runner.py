import sys
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from functools import wraps
from itertools import takewhile
from typing import Any, ParamSpec, overload

from utils.common import should_bypass_timeout
from utils.time import format_minimal_seconds


def truncate_param(arg, max_str=100, max_seq=10):
    if isinstance(arg, str):
        return "'" + arg + "'" if len(arg) <= max_str else "'" + arg[:max_str] + "...'"
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


P = ParamSpec("P")


# Overload 1: Called with arguments or parens -> returns a Decorator
@overload
def pretty_test_runner(
    time_limit_in_sec: float | None = ...,
    stop_on_tc_failure: bool | None = ...,
) -> Callable[[Callable[P, tuple[bool, str]]], Callable[P, tuple[bool, str]]]: ...


# Overload 2: Used directly as a bare decorator `@pretty_test_runner`
@overload
def pretty_test_runner(
    time_limit_in_sec: Callable[P, tuple[bool, str]],
    stop_on_tc_failure: bool | None = ...,
) -> Callable[P, tuple[bool, str]]: ...


def pretty_test_runner(
    time_limit_in_sec: Any = None, stop_on_tc_failure: bool | None = False
) -> Any:
    """
    Decorator for test functions that formats output, handles timeouts, and optionally
    halts execution on failure.
    """
    target_func: Any = None
    actual_time_limit_in_sec: float | None = None

    if callable(time_limit_in_sec) and not isinstance(time_limit_in_sec, (int, float)):
        target_func = time_limit_in_sec
        actual_time_limit_in_sec = None
    elif isinstance(time_limit_in_sec, (int, float)):
        actual_time_limit_in_sec = float(time_limit_in_sec)
    else:
        actual_time_limit_in_sec = None

    # If debugging, ignore the timeout completely.
    if should_bypass_timeout():
        actual_time_limit_in_sec = None

    def decorator(func: Callable[P, tuple[bool, str]]) -> Callable[P, tuple[bool, str]]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> tuple[bool, str]:
            # Print [RUN] <args>
            fmt_args = [truncate_param(a) for a in args]
            fmt_kwargs = {k: truncate_param(v) for k, v in kwargs.items()}
            args_str = ", ".join(map(str, fmt_args))
            kwargs_str = ", ".join(f"{k}={v}" for k, v in fmt_kwargs.items())
            all_args_str = ", ".join(filter(None, [args_str, kwargs_str]))
            print(f"[RUN] {func.__name__}({all_args_str})")

            passed = False
            error_msg = None

            start_time = time.perf_counter()

            if actual_time_limit_in_sec is not None and actual_time_limit_in_sec > 0:
                # Execute test function with a timeout using ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(func, *args, **kwargs)
                    try:
                        result = future.result(timeout=actual_time_limit_in_sec)
                        # Expecting function return: (bool_status, str_error_msg)
                        if isinstance(result, tuple) and len(result) == 2:
                            passed, error_msg = result
                        else:
                            passed = bool(result)
                            error_msg = "Test returned unexpected format (expected tuple: (bool, str))."
                    except TimeoutError:
                        passed = False
                        error_msg = (
                            f"Test timed out after {actual_time_limit_in_sec} seconds."
                        )
            else:
                result = func(*args, **kwargs)
                if isinstance(result, tuple) and len(result) == 2:
                    passed, error_msg = result
                else:
                    passed = bool(result)
                    error_msg = (
                        "Test returned unexpected format (expected tuple: (bool, str))."
                    )
            duration = time.perf_counter() - start_time

            # Format and print results according to rules
            if passed:
                print(f"[DONE] ({format_minimal_seconds(duration)})")
            else:
                if error_msg:
                    print(f"Error: {error_msg}")
                print(f"[FAILED] ({format_minimal_seconds(duration)})")

                if stop_on_tc_failure:
                    print(
                        "Stopping execution due to test failure (stop_on_tc_failure=True)."
                    )
                    sys.exit(1)

            return passed, error_msg

        return wrapper

    # Allow decorator to be used either with or without parentheses: @PrettyTestRun or @PrettyTestRun(...)
    if target_func is not None:
        return decorator(target_func)

    return decorator


def eq_list_int(
    actual: list[int] | None, expected: list[int] | None
) -> tuple[bool, str]:
    if not actual and not expected:
        return True, ""
    if actual and not expected:
        return False, "actual and not expected"
    if not actual and expected:
        return False, "not actual and expected"
    n = len(expected)
    if n != len(actual):
        return False, f"len(actual) = {len(actual)}, len(expected) = {n}"
    num_matches = sum(
        1
        for _ in takewhile(
            lambda pair: pair[0] == pair[1],
            zip(actual, expected),
        )
    )
    if num_matches < n:
        return (
            False,
            f"actual={truncate_param(actual)}\nactual[{num_matches}] != expected[{num_matches}]",
        )
    return True, ""


def main():
    assert eq_list_int(actual=[1, 2, 3], expected=[1, 2, 3])[0]
    assert not eq_list_int(actual=[1, 2], expected=[1, 2, 3])[0]
    assert eq_list_int(None, None)[0]
    assert not eq_list_int(None, [1])[0]
    assert not eq_list_int([1], None)[0]
    assert not eq_list_int(actual=[1, 4, 3], expected=[1, 2, 3])[0]


if __name__ == "__main__":
    main()
