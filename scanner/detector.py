from pathlib import Path

STRONG_SIGNALS = [
    ".git",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Cargo.toml",
    "go.mod",
]

IGNORE_FOLDERS = {
    "node_modules",
    "vendor",
    "dist",
    "build",
    ".cache",
    "venv",
    "__pycache__",
}


def is_project(folder: Path) -> bool:
    """
    Returns True if folder contains strong development signals.
    """
    if not folder.is_dir():
        return False

    if folder.name in IGNORE_FOLDERS:
        return False

    for signal in STRONG_SIGNALS:
        if (folder / signal).exists():
            return True

    return False


def find_projects(space_path: str):
    """
    Scan top-level directories inside space and detect projects.
    """
    space = Path(space_path)

    if not space.exists():
        raise ValueError(f"Path does not exist: {space_path}")

    projects = []

    for item in space.iterdir():
        if is_project(item):
            projects.append(item)

    return projects