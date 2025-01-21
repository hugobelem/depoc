from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from django.utils import timezone

from datetime import datetime, timedelta

import calendar

from modules.business.models import Business

from . import error


def get_user_business(user: Request) -> (
        tuple[Business, None] |
        tuple[None, dict]
    ):
    """
    Helper function to retrieve the business associated with the owner.
    Returns a tuple (business, error_response), where one is None.
    """
    if hasattr(user, 'owner'):
        business = getattr(user.owner, 'business')
    elif hasattr(user, 'member'):
        business = getattr(user.member, 'business')

    if not business:
        error_response = error.builder(404, 'Owner does not have a business.')
        return None, error_response
    
    return business, None


def paginate(data, request: Request, page_size: int) -> Response:
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    
    paginated_data = paginator.paginate_queryset(data, request)
    
    return paginator.get_paginated_response(paginated_data)


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
