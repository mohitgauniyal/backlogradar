import sys
from scanner.walker import walk_space
from scanner.activity import (
    get_git_last_commit,
    get_git_recent_commits,
    get_filesystem_last_modified,
    get_file_modified_time,
)
from scanner.status import calculate_status
from logger import setup_logger

logger = setup_logger()


def scan(space_path: str):
    logger.info(f"Starting scan for space: {space_path}")

    projects, duration = walk_space(space_path)

    logger.info(f"Detected {len(projects)} projects (including archives)")

    status_counts = {
        "Active": 0,
        "Warm": 0,
        "Cold": 0,
        "Frozen": 0,
        "Unknown": 0,
        "Archived": 0,
    }

    for record in projects:
        project = record.path
        project_type = record.project_type

        print("\n" + "=" * 60)
        print(f"Project: {project.name}")
        print(f"Type: {project_type}")

        if project_type != "archived":
            print(f"Ecosystem: {record.ecosystem or 'Unknown'}")
            print(f"Version Control: {'Git' if record.has_git else 'None'}")

        git_activity = None

        if project_type == "archived":
            last_activity = get_file_modified_time(project)
            source = "Zip Archive"
            recent_commits = []
            status_counts["Archived"] += 1

        else:
            if record.has_git:
                git_activity = get_git_last_commit(project)

            if git_activity:
                last_activity = git_activity
                source = "Git"
                recent_commits = get_git_recent_commits(project, limit=3)
            else:
                last_activity = get_filesystem_last_modified(project)
                source = "Filesystem"
                recent_commits = []

        status, days_ago = calculate_status(last_activity)

        if project_type != "archived":
            status_counts[status] += 1

        print(f"Last Activity: {last_activity}")
        print(f"Days Ago: {days_ago}")
        print(f"Status: {status}")
        print(f"Source: {source}")

        if recent_commits:
            print("\nRecent Commits:")
            for commit in recent_commits:
                print(
                    f"  {commit['hash']} | {commit['date']} | {commit['message']}"
                )

        print("=" * 60)

    # ---- Summary Section ----
    print("\n" + "#" * 60)
    print("SCAN SUMMARY")
    print("#" * 60)

    print(f"Total Projects Found: {len(projects)}")
    print(f"Active: {status_counts['Active']}")
    print(f"Warm: {status_counts['Warm']}")
    print(f"Cold: {status_counts['Cold']}")
    print(f"Frozen: {status_counts['Frozen']}")
    print(f"Unknown: {status_counts['Unknown']}")
    print(f"Archived (zip): {status_counts['Archived']}")
    print(f"Scan Duration: {duration} seconds")
    print("#" * 60 + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "scan":
        print("Usage: python main.py scan <path>")
        sys.exit(1)

    scan(sys.argv[2])
