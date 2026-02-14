from pathlib import Path
from scanner.constants import PROJECT_SIGNALS, GIT_SIGNAL


def detect_project(folder: Path):
    """
    Detects whether a folder is a project.
    Returns (is_project: bool, ecosystem: str or None)
    Fully safe against filesystem errors.
    """

    if not folder.is_dir():
        return False, None

    # signal: Git
    try:
        if (folder / GIT_SIGNAL).exists():
            return True, "git"
    except (PermissionError, OSError):
        return False, None

    # Structured ecosystem detection
    for ecosystem, signals in PROJECT_SIGNALS.items():
        for signal in signals:
            try:
                if (folder / signal).exists():
                    return True, ecosystem
            except (PermissionError, OSError):
                return False, None

    return False, None


def is_zip_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() == ".zip"
