from pathlib import Path
from scanner.constants import STRONG_SIGNALS


def is_project(folder: Path) -> bool:
    """
    Conservative project detection.
    Fully protected against filesystem permission errors.
    """
    if not folder.is_dir():
        return False

    for signal in STRONG_SIGNALS:
        try:
            if (folder / signal).exists():
                return True
        except (PermissionError, OSError):
            # If we cannot access inside this folder, treat as non-project
            return False

    return False


def is_zip_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() == ".zip"
