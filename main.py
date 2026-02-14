import sys
from scanner.walker import walk_space
from scanner.activity import (
    get_git_last_commit,
    get_filesystem_last_modified,
)
from scanner.status import calculate_status
from logger import setup_logger

logger = setup_logger()


def scan(space_path: str):
    logger.info(f"Starting scan for space: {space_path}")

    projects, duration = walk_space(space_path)

    logger.info(f"Detected {len(projects)} projects (including archives)")

    for record in projects:
        project = record.path
        project_type = record.project_type

        logger.info(f"Scanning: {project.name} ({project_type})")

        if project_type == "archived":
            last_activity = get_filesystem_last_modified(project.parent)
            source = "Zip archive"
        else:
            git_activity = get_git_last_commit(project)

            if git_activity:
                last_activity = git_activity
                source = "Git"
            else:
                last_activity = get_filesystem_last_modified(project)
                source = "Filesystem"

        status, days_ago = calculate_status(last_activity)

        logger.info(
            f"{project.name} | {status} | {days_ago} days ago | Source: {source}"
        )

    logger.info(f"Scan completed in {duration} seconds.")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "scan":
        print("Usage: python main.py scan <path>")
        sys.exit(1)

    scan(sys.argv[2])
