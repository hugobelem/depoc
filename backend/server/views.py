from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_routes(request):
    routes = [
        'http://127.0.0.1:8000/api/token',
        'http://127.0.0.1:8000/api/token/refresh',
    ]
    return Response(routes)