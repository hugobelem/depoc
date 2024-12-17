from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.contrib.auth import get_user_model

from .serializers import UserSerializer

from datetime import timedelta, datetime

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
        '''
        Schedules account deletion with a 90-day grace period.
        * Background task not implemented yet.
        '''
        User.objects.get(id=request.user.id).delete()
        today = datetime.today()        
        deletion_date = (today + timedelta(days=90)).strftime('%B %d, %Y')  
        message = (
            'Your account is scheduled for deletion. '
            f'Log in before {deletion_date}, to restore it. '
        )                    
        return Response(
            {'detail': message}, 
            status=status.HTTP_202_ACCEPTED
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