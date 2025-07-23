from datetime import datetime, timezone

def get_current_datetime():
    """
    Returns the current UTC datetime as a timezone-aware object.
    """
    return datetime.now(timezone.utc)
