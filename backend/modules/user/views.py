from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.contrib.auth import get_user_model

from .serializers import UserSerializer

User = get_user_model()


class Me(APIView):
    '''
    API view to manage authenticated merchant's data.
    '''
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

