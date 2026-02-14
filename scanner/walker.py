import time
from pathlib import Path
from scanner.constants import (
    IGNORE_FOLDERS,
    SYSTEM_IGNORE_FOLDERS,
    MAX_DEPTH,
)
from scanner.detector import is_project, is_zip_file


class ProjectRecord:
    def __init__(self, path: Path, project_type: str):
        self.path = path
        self.project_type = project_type  # "normal" or "archived"


def should_ignore(folder: Path) -> bool:
    """
    Determines if a folder should be ignored.
    """
    if folder.name.lower() in {f.lower() for f in IGNORE_FOLDERS}:
        return True

    if folder.name.lower() in {f.lower() for f in SYSTEM_IGNORE_FOLDERS}:
        return True

    return False


def walk_space(space_path: str):
    """
    Controlled recursive project detection.
    Stops descending once a project is found.
    """

    space = Path(space_path)

    if not space.exists():
        raise ValueError(f"Path does not exist: {space_path}")

    # Disallow scanning C:\
    if space.drive.upper() == "C:" and space == Path("C:/"):
        raise PermissionError("Scanning C:\\ root is not allowed.")

    projects = []

    start_time = time.time()

    def walk(current_path: Path, depth: int):
        if depth > MAX_DEPTH:
            return

        if not current_path.is_dir():
            return

        if should_ignore(current_path):
            return

        # Detect project
        try:
            if is_project(current_path):
                projects.append(ProjectRecord(current_path, "normal"))
                return
        except (PermissionError, OSError):
            return

        try:
            children = list(current_path.iterdir())
        except (PermissionError, OSError):
            # Skip folders we cannot access
            return

        # Detect zip archives
        for child in children:
            if is_zip_file(child):
                projects.append(ProjectRecord(child, "archived"))

        # Continue recursion
        for child in children:
            if child.is_dir():
                walk(child, depth + 1)

    walk(space, depth=0)

    duration = round(time.time() - start_time, 2)

    return projects, duration
