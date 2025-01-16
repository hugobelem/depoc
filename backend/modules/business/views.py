from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BusinessSerializer

from shared import (
    error,
    validate,
    BurstRateThrottle,
    SustainedRateThrottle,
    get_user_business,
    IsOwner,
)


class BusinessEndpoint(APIView):
    permission_classes = [IsOwner]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)

        serializer = BusinessSerializer(business)

        return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        owner = request.user.owner

        invalid_params = validate.params(request, BusinessSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer = BusinessSerializer(data=data, context={'owner': owner})
        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
    

    def patch(self, request):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_params = validate.params(request, BusinessSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer = BusinessSerializer(instance=business, data=data, partial=True)
        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        business.is_active = False
        business.save()

        data = {
            'business': {
                'is_active': False
            }
        }

        return Response(data, status.HTTP_200_OK)
