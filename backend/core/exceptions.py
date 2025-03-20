from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

import os


is_production = os.getenv('ENVIRONMENT') == 'production'

def handler(exc, context):
    response = exception_handler(exc, context)

    if response:
        data = {
            'error': {
                'status': response.status_code,
                'message': response.data.get('detail', 'An error occurred.'),
            }
        }
        return Response(data, status=response.status_code)
    
    elif not response and is_production:
        data = {
            'error': {
                'status': 500,
                'message': 'An unexpected error occurred.',
            }
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
