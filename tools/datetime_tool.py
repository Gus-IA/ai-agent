from datetime import datetime


def get_current_datetime() -> str:
    """Returns the current date and time."""
    now = datetime.now()
    return now.strftime("Today is %A, %B %d, %Y. Current time: %H:%M:%S")
