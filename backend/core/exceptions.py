from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

import os
import logging


logger = logging.getLogger(__name__)
is_production = os.getenv('ENVIRONMENT') == 'production'

def handler(exc, context):
    response = exception_handler(exc, context)
    logger.error(f'EXCEPTION OCCURRED: {response}')

    if response:
        data = {
            'error': {
                'status': response.status_code,
                'message': response.data.get('detail', 'An error occurred.'),
            }
        }
        return Response(data, status=response.status_code)
    
    elif not response and is_production:
        logger.error(f'EXCEPTION IN PROD OCCURRED: {response}')
        data = {
            'error': {
                'status': 500,
                'message': 'An error occurred.',
            }
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
