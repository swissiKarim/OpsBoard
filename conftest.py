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
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q",
             "-r", str(req), "--break-system-packages"],
            check=True,
        )
        # Ensure user site-packages is on sys.path for the current process
        import site
        user_site = site.getusersitepackages()
        if user_site not in sys.path:
            sys.path.insert(0, user_site)
