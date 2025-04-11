from datetime import datetime, timedelta


def find_previous_cycle_time(time: datetime, cycle_period_hours: int) -> datetime:
    """Find the previous rounded cycle time given the current time.

    Args:
        time (datetime): The current time
        cycle_period_hours (int): The cycle period in hours

    Returns:
        datetime: The previous time in the cycle

    """
    midnight = time.replace(hour=0, minute=0, second=0, microsecond=0)
    hours_passed = (time - midnight).total_seconds() / 3600
    cycles_passed = int(hours_passed / cycle_period_hours)
    return midnight + timedelta(hours=cycles_passed * cycle_period_hours)
