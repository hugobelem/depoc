from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.contrib.auth import get_user_model

from .serializers import UserSerializer

User = get_user_model()


class Me(APIView):
    '''
    API view to manage authenticated user's data.

    - Retrieve.
    - Update.
    - Delete.
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):      
        user = request.user
        data = request.data
        serializer = UserSerializer(user, data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        user = request.user
        user.delete()
        return Response(
            {'detail': 'User deleted successfully.'}, 
            status=status.HTTP_204_NO_CONTENT
        )


class CreateUser(APIView):
    '''
    API view to create a new user.
    '''
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {'detail': 'User created successfully.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)