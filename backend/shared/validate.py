"""
This module provides a utility function to validate request parameters against 
a serializer's defined fields.

Function:
- params(request, serializer): Checks if the parameters in the request match 
  the fields defined in the serializer, excluding the 'id' field.
"""

from rest_framework.serializers import ModelSerializer
from rest_framework.request import Request


def params(
        request: Request,
        serializer: ModelSerializer,
        add: str | None = None,
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

    request_params = set(request.data.keys())
    invalid_params = request_params - fields

    if invalid_params:
        return invalid_params
    
    return None
