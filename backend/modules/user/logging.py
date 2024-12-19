'''
Logging Module for User Actions.

Functions:
    log_field_errors(request, invalid_fields):
        Logs field errors during a user creation or update request.
        
    log_password_attempt(user, request):
        Logs password update attempts that are not allowed through the endpoint.
'''

import logging


logger = logging.getLogger(__name__)

def log_field_errors(request, field_errors: set) -> None:
    '''
    Logs field errors during a user creation or update request.

    This function logs a warning message including:
    - timestamp
    - user ID
    - details of the attempted action
    - endpoint where the action was attempted      
    '''    
    msg = (
        f'User "{request.user.id}" '
        'attempted to update with invalid or missing fields: '
        f'"{', '.join(field_errors)}". '
    )
    logger.warning(msg)


def log_password_attempt(request) -> None:
    '''
    Logs an attempt to modify the user's password,
    which is not allowed through the endpoint.

    This function logs a warning message including:
    - timestamp
    - user ID
    - endpoint where the action was attempted   
    '''
    msg = (
        f'User "{request.user.id}" '
        'attempted to modify the password. '
    )
    logger.warning(msg)

