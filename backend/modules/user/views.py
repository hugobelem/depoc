from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.contrib.auth import get_user_model

from .serializers import SuperUserSerializer

User = get_user_model()


class CreateMerchant(APIView):
    '''
    API view to manage authenticated merchant's data.
    '''
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, format=None):
        user = SuperUserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_200_OK)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


class Merchant(APIView):
    '''
    API view to manage authenticated merchant's data.
    '''
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        user = request.user
        serializer = SuperUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        user = SuperUserSerializer(
            instance=request.user, data=request.data, partial=True
        )
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_200_OK)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
