"""Windows compatibility shim for gltest temporary stdin cleanup."""
import os
import sys

if sys.platform == "win32":
    _unlink = os.unlink

    def _windows_unlink(path, *args, **kwargs):
        try:
            return _unlink(path, *args, **kwargs)
        except PermissionError:
            if os.path.basename(path).startswith("tmp"):
                return None
            raise

    os.unlink = _windows_unlink
