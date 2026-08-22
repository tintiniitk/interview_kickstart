import builtins
import sys


def is_debugging() -> bool:
    """
    Check if Python is running under an active debugger (VS Code debugpy, pdb, pydevd).
    """
    # 1. Standard Python trace check (works for pdb and standard tracers)
    if sys.gettrace() is not None:
        return True

    # 2. Check if debugpy or pydevd engine is loaded in active modules
    return "debugpy" in sys.modules or "pydevd" in sys.modules


def is_profiling() -> bool:
    """Check if Python is running under line_profiler / kernprof or cProfile."""
    # kernprof injects 'profile' into builtins at runtime
    if hasattr(builtins, "profile"):
        return True
    # Check if line_profiler or cProfile modules are actively imported/running
    return "line_profiler" in sys.modules or "cProfile" in sys.modules


def should_bypass_timeout() -> bool:
    """Returns True if timeout protections should be disabled (debugging or profiling)."""
    return is_debugging() or is_profiling()
