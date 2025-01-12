"""
Ensure consistent error handling and communication of error details to clients.

Functions:
- builder: Constructs a standardized error response dictionary.
"""

def builder(
        status: int,
        message: str,
        details=None,
        **kwargs
    ) -> dict:

    """
    Constructs a standardized error response dictionary.

    Args:
        status (int): HTTP status code.
        message (str): A brief description of the error.
        details (Optional[Any]): Additional details about the error (default is None).
        **kwargs: Additional optional key-value pairs to include in the error response.

    Returns:
        dict: A dictionary representing the structured error response.

    Example:
        >>> build_error_response(400, "Invalid input.", details="Missing field 'name'")
        {
            "error": {
                "status": 400,
                "message": "Invalid input.",
                "details": "Missing field 'name'"
            }
        }
    """

    response = {
        'error': {
            'status': status,
            'message': message,
        }
    }

    if details:
        response['error'].update({'details': details})

    for value in kwargs.values():
        if value:
            response['error'].update(**kwargs)
    
    return response
