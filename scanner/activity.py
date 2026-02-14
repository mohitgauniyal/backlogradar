import subprocess
from pathlib import Path
from datetime import datetime
from scanner.constants import IGNORE_FOLDERS

def get_git_recent_commits(project_path: Path, limit: int = 3):
    """
    Returns last N commits as list of dicts:
    [{hash, message, date}]
    """
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(project_path),
                "log",
                f"-{limit}",
                "--pretty=format:%H|%cd|%s",
                "--date=iso-strict",
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )

        lines = result.stdout.strip().split("\n")
        commits = []

        for line in lines:
            if not line.strip():
                continue

            commit_hash, date_str, message = line.split("|", 2)
            dt = datetime.fromisoformat(date_str).replace(tzinfo=None)

            commits.append(
                {
                    "hash": commit_hash[:7],
                    "date": dt,
                    "message": message,
                }
            )

        return commits

    except Exception:
        return []


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

def get_file_modified_time(file_path: Path):
    """
    Returns file modification time safely.
    """
    try:
        return datetime.fromtimestamp(file_path.stat().st_mtime)
    except Exception:
        return None
