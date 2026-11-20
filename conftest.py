"""Root conftest: ensure dependencies are installed before test collection."""
import subprocess
import sys
from pathlib import Path


def pytest_configure(config):
    """Install requirements if fastapi is not yet importable."""
    try:
        import fastapi  # noqa: F401
    except ImportError:
        req = Path(__file__).parent / "requirements.txt"
        if req.exists():
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-q",
                 "-r", str(req), "--break-system-packages"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
