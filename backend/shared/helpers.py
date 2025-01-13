from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

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
    business = getattr(user.owner, 'business', None)
    print(type(business))

    if not business:
        error_response = error.builder(404, 'Owner does not have a business.')
        return None, error_response
    
    return business, None


def paginate(data, request: Request, page_size: int) -> Response:
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    
    paginated_data = paginator.paginate_queryset(data, request)
    
    return paginator.get_paginated_response(paginated_data)
