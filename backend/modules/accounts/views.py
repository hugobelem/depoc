from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .serializers import UserSerializer, OwnerSerializer

from shared import (
    error,
    validate,
    BurstRateThrottle,
    SustainedRateThrottle,
    IsOwner,
)


class MeEndpoint(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


class AccountsEndpoint(APIView):
    def get_throttles(self):
        method = self.request.method
        if method == 'POST':
            return [AnonRateThrottle()]
        else:
            return [BurstRateThrottle(), SustainedRateThrottle()]


    def get_permissions(self):
        method = self.request.method
        if method == 'POST':
            return [permissions.AllowAny()]
        elif method in ('GET', 'PATCH'):
            return [permissions.IsAuthenticated()]
        else:
            return [IsOwner()]
        

    def post(self, request):
        data = request.data
        invalid_params = validate.params(request, UserSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        
        return Response(serializer.data, status.HTTP_201_CREATED)
    

    def patch(self, request):
        data = request.data
        user = request.user

        params = data.keys()
        if 'password' in params:
            message = 'Unable to update the password through this endpoint.'
            error_response = error.builder(400, message)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

        invalid_params = validate.params(request, UserSerializer)
        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(instance=user, data=data, partial=True)
        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)         

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()

        data = {
            'user': {'id': user.id, 'is_active': False}
        }

        return Response(data, status.HTTP_200_OK)


class OwnerEndpoint(APIView):
    permission_classes = [IsOwner]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request):
        user = request.user
        owner = user.owner  
        serializer = OwnerSerializer(owner)

        return Response(serializer.data, status.HTTP_200_OK)


    def patch(self, request):
        data = request.data
        user = request.user
        owner = user.owner

        invalid_params = validate.params(request, OwnerSerializer)
        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer = OwnerSerializer(instance=owner, data=data, partial=True)
        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)
