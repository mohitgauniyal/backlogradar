import subprocess
from pathlib import Path
from datetime import datetime

IGNORE_FOLDERS = {
    "node_modules",
    "vendor",
    "dist",
    "build",
    ".cache",
    "venv",
    "__pycache__",
}

def get_git_last_commit(project_path: Path):
    """
    Returns last commit datetime if git repo.
    Converts to naive local datetime for safe comparison.
    """
    try:
        result = subprocess.run(
    ["git", "-C", str(project_path), "log", "-1", "--format=%cd", "--date=iso-strict"],
    capture_output=True,
    text=True,
    check=True,
    timeout=5  # prevent hanging
)

        date_str = result.stdout.strip()

        # Parse ISO with timezone
        dt = datetime.fromisoformat(date_str)

        # Convert to naive (remove timezone)
        return dt.replace(tzinfo=None)

    except Exception:
        return None


def get_filesystem_last_modified(project_path: Path):
    """
    Safer filesystem fallback with ignore rules.
    """
    latest_time = None

    for path in project_path.rglob("*"):
        # Skip ignored folders
        if any(part in IGNORE_FOLDERS for part in path.parts):
            continue

        if path.is_file():
            try:
                modified_time = datetime.fromtimestamp(path.stat().st_mtime)

                if latest_time is None or modified_time > latest_time:
                    latest_time = modified_time
            except Exception:
                continue

    return latest_time