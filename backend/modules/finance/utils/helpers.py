from django.utils import timezone

from datetime import datetime, timedelta

import calendar


def get_start_and_end_date(
        today: datetime,
        week: bool | None = None,
        month: bool | None = None,
    ) -> tuple[datetime, datetime]:
    """
    Determines the start and end dates of a specified time period.

    This helper function calculates the start and end dates for either:
    - The current week, if `week=True`.
    - The current month, if `month=True`.

    ### Date Format:
    - Start date: `YYYY-MM-DD 00:00:00±[HH:MM]`
    - End date: `YYYY-MM-DD 23:59:59±[HH:MM]`

    ### Returns:
    - A tuple of `datetime` objects: `(start_date, end_date)`.
    """
    if week:
        weekday = today.weekday()
        start_date = today - timedelta(days=weekday)
        end_date = start_date + timedelta(days=6)
    elif month:
        start_date = today.replace(day=1)
        end_date = today.replace(
            day=calendar.monthrange(today.year, today.month)[1]
        )
    elif week == month:
        raise ValueError("Exactly one of 'week' or 'month' must be set to True.")

    start_date = timezone.make_aware(
        start_date.replace(hour=0, minute=0, second=0, microsecond=0),
        timezone.get_current_timezone()
    )
    end_date = timezone.make_aware(
        end_date.replace(hour=23, minute=59, second=59, microsecond=0),
        timezone.get_current_timezone()
    )

    return start_date, end_date
