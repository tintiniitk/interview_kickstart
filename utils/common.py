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
