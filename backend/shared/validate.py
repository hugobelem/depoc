"""
This module provides a utility function to validate request parameters against 
a serializer's defined fields.

Function:
- params(request, serializer): Checks if the parameters in the request match 
  the fields defined in the serializer, excluding the 'id' field.
- date(date, ignore): Checks if the date is in the following format: YYYY-MM-DD.
"""

from rest_framework.serializers import ModelSerializer
from rest_framework.request import Request

import re


def params(
        request: Request,
        serializer: ModelSerializer,
        add: str | None = None,
        remove: list[str] | None = None,
    ) -> set | None:
    """
    Checks if the parameters in the request match 
    the fields defined in the serializer, excluding the 'id' field.

    Returns:
        set: A set containing the invalid parameters, if any.
        None: Returned if all parameters are valid.
    """
    serializer = serializer()
    fields = set(serializer.fields.keys())
    fields.discard('id')

    if add:
        fields.add(add)

    if remove:
        if not isinstance(remove, list):
            raise ValueError('Remove has to be a list')
        fields.difference_update(remove)

    request_params = set(request.data.keys())
    invalid_params = request_params - fields

    if invalid_params:
        return invalid_params
    
    return None


def date(date: str, ignore: list[str] | None = None) -> bool:
    """
    Checks if the date is in the following format:
    YYYY-MM-DD
    - ignore: List of str that should be ignored during validation
    """
    r = re.compile('\d{4}-\d{2}-\d{2}')
    valid_format = r.match(date) is not None
    valid_length = len(date) == 10

    if ignore and date in ignore:
        return True

    if valid_format and valid_length:
        return True
    
    return False
