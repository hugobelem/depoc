from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import SuperUserSerializer

User = get_user_model()


class MeEndpoint(APIView):
    '''
    API view to get authenticated owner's data.
    '''
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        user = request.user
        serializer = SuperUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)    


class OwnerEndpoint(APIView):
    '''
    API view to manage authenticated owner's data.
    '''
    def check_field_errors(self, request, check_missing=False) -> set | None:
        request_fields = set(request.data.keys())
        valid_fields = set(SuperUserSerializer.Meta.fields)

        invalid_fields = request_fields - valid_fields
        if invalid_fields:
            return invalid_fields
        
        if check_missing:
            required_fields = set(SuperUserSerializer.Meta.required)
            missing_fields = required_fields - request_fields
            if missing_fields:
                return missing_fields

        return None


    def get_permissions(self):
        method = self.request.method
        if method == 'POST':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]


    def post(self, request, format=None):    
        data = request.data
        if not data:
            return Response(
                {'error': 'No data provided for Owner creation.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        field_errors = self.check_field_errors(request, check_missing=True)
        if field_errors:
            message = {
                    'error': f'Invalid or missing fields: {", ".join(field_errors)}',
                    'expected': SuperUserSerializer.Meta.required
                },
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        serializer = SuperUserSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )   

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)     


    def patch(self, request, format=None):
        user = request.user
        data = request.data
        if not data:
            return Response(
                {'error': 'No data provided for the update.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        field_errors = self.check_field_errors(request)
        if field_errors:
            message = {
                    'error': f'Invalid fields: {", ".join(field_errors)}',
                    'expected': SuperUserSerializer.Meta.required
                },
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = SuperUserSerializer(
            instance=user,
            data=data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )            
        
        if 'password' in serializer.validated_data:
            return Response(
                {
                    'error': 
                    'Password modification is not allowed through this endpoint.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )            

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def delete(self, request, format=None):
        user = get_object_or_404(User, id=request.user.id)
        user.is_active = False
        user.save()
        return Response(
            {'success:': 'User is inactive'},
            status=status.HTTP_200_OK
        )

