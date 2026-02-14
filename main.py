import sys
from pathlib import Path
from scanner.detector import find_projects
from scanner.activity import get_git_last_commit, get_filesystem_last_modified
from scanner.status import calculate_status
from logger import setup_logger

logger = setup_logger()


def scan(space_path: str):
    logger.info(f"Starting scan for space: {space_path}")

    projects = find_projects(space_path)

    logger.info(f"Detected {len(projects)} potential projects")

    if not projects:
        logger.warning("No projects found.")
        return

    for project in projects:
        logger.info(f"Scanning project: {project.name}")

        git_activity = get_git_last_commit(project)

        if git_activity:
            last_activity = git_activity
            activity_source = "Git"
            logger.info("Using Git activity")
        else:
            logger.info("No git activity found, using filesystem fallback")
            last_activity = get_filesystem_last_modified(project)
            activity_source = "Filesystem"

        status, days_ago = calculate_status(last_activity)

        logger.info(
            f"{project.name} | Status: {status} | Days ago: {days_ago} | Source: {activity_source}"
        )

    logger.info("Scan completed.")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "scan":
        print("Usage: python main.py scan <path>")
        sys.exit(1)

    scan(sys.argv[2])
