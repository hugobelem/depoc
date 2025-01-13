from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BusinessSerializer

from shared import (
    error,
    validate,
    BurstRateThrottle,
    SustainedRateThrottle
)

def has_business(request):
    business = request.user.owner.business
    
    if not business:
        error_response = error.builder(404, 'Owner does not have a business.')
        return Response(error_response, status.HTTP_404_NOT_FOUND)

    return business


class BusinessEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request):
        business = has_business(request)

        if isinstance(business, Response):
            return business

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
        business = request.user.owner.business

        if not business:
            message = 'Owner does not have a business.'
            error_response = error.builder(404, message)
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
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
        business = request.user.owner.business

        if not business:
            message = 'Owner does not have a business.'
            error_response = error.builder(404, message)
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        business.is_active = False
        business.save()

        data = {
            'business': {
                'is_active': False
            }
        }

        return Response(data, status.HTTP_200_OK)
