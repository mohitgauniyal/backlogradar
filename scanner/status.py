from datetime import datetime


def calculate_status(last_activity: datetime):
    if not last_activity:
        return "Unknown", None

    now = datetime.now()
    days_ago = (now - last_activity).days

    if days_ago <= 7:
        return "Active", days_ago
    elif days_ago <= 30:
        return "Warm", days_ago
    elif days_ago <= 90:
        return "Cold", days_ago
    else:
        return "Frozen", days_ago