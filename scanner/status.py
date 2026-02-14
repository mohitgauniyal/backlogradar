from datetime import datetime
from scanner.constants import STATUS_THRESHOLDS


def calculate_status(last_activity: datetime):
    if not last_activity:
        return "Unknown", None

    days_ago = (datetime.now() - last_activity).days

    if days_ago <= STATUS_THRESHOLDS["ACTIVE"]:
        return "Active", days_ago
    elif days_ago <= STATUS_THRESHOLDS["WARM"]:
        return "Warm", days_ago
    elif days_ago <= STATUS_THRESHOLDS["COLD"]:
        return "Cold", days_ago
    else:
        return "Frozen", days_ago
