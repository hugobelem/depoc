from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import SuperUserSerializer

User = get_user_model()


class GetMe(APIView):
    '''
    API view to get authenticated owner's data.
    '''
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        user = request.user
        serializer = SuperUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)    


class Owner(APIView):
    '''
    API view to manage authenticated owner's data.
    '''
    def get_permissions(self):
        method = self.request.method
        if method == 'POST':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]
        
    def post(self, request, format=None):
        user = SuperUserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_201_CREATED)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)        

    def patch(self, request, format=None):
        request_fields = set(request.data.keys())
        valid_fields = set(SuperUserSerializer.Meta.fields)
        invalid_fields = request_fields - valid_fields

        if invalid_fields:
            return Response(
                {'error': f'Invalid fields: {", ".join(invalid_fields)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = SuperUserSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )

        if user.is_valid():
            if 'password' in user.validated_data:
                return Response(
                    {
                        'error': 
                        'Password modification is not allowed through this endpoint.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.save()
            return Response(user.data, status=status.HTTP_200_OK)
    
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        user = get_object_or_404(User, id=request.user.id)
        user.is_active = False
        user.save()
        return Response(
            {'detail:': 'User is inactive'},
            status=status.HTTP_200_OK)

