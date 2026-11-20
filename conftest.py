"""Root conftest: ensure dependencies are installed before test collection."""
import subprocess
import sys
from pathlib import Path


def pytest_configure(config):
    """Install requirements if key deps are not yet importable."""
    try:
        import sqlalchemy  # noqa: F401
        import fastapi  # noqa: F401
    except ImportError:
        req = Path(__file__).parent / "requirements.txt"
        if not req.exists():
            return
        # Try system-wide first (CI often runs as root)
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-r", str(req)],
        )
        if r.returncode != 0:
            # Fallback: user install with PEP-668 override
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-q",
                 "-r", str(req), "--break-system-packages"],
                check=True,
            )
