from datetime import datetime


def get_missing_days(limit_day):
    try:
        date_now = datetime.now().date()
        missing_days = (limit_day - date_now).days
        if missing_days < 1:
            missing_days = 0
        return missing_days
    except Exception as e:
        return 0
