from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from . import services
from .throttling import BurstRateThrottle, SustainedRateThrottle
from .serializers import TransactionSerializer

class TransactionEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def post(self, request):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        data = services.get_data(request)
        if isinstance(data, Response):
            error_response = data
            return error_response
        
        if field_errors := services.check_field_errors(
                request,
                TransactionSerializer,
            ):
            return field_errors
        
        serializer = TransactionSerializer(
            data=data,
            context={'business': business},
        )

        if not serializer.is_valid():
            message = 'Validation failed: '
            return Response(
                {'error': message, 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)