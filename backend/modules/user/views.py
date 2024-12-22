from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, throttling
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import SuperUserSerializer

User = get_user_model()


class MeEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        user = request.user
        serializer = SuperUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)    


class OwnerEndpoint(APIView):
    def check_field_errors(self, request, check_missing=False) -> set | None:
        request_fields = set(request.data.keys())
        valid_fields = set(SuperUserSerializer.Meta.fields)
        invalid_fields = request_fields - valid_fields
        if invalid_fields:
            return invalid_fields
        
        required_fields = set(SuperUserSerializer.Meta.post_required)
        missing_fields = required_fields - request_fields
        if missing_fields and check_missing:
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
            message = 'No data provided for Owner creation.'
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

        field_errors = self.check_field_errors(request, check_missing=True)
        if field_errors:
            message = f'Invalid or missing fields: {", ".join(field_errors)}'
            expected_fields = SuperUserSerializer.Meta.fields
            return Response(
                {'error': message, 'expected': expected_fields},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SuperUserSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )   

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)     


    def patch(self, request, format=None):
        data = request.data
        if not data:
            message = 'No data provided for the update.'
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

        field_errors = self.check_field_errors(request)
        if field_errors:
            message = f'Invalid fields: {", ".join(field_errors)}'
            expected_fields = SuperUserSerializer.Meta.patch_required
            return Response(
                {'error': message, 'expected': expected_fields},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        serializer = SuperUserSerializer(instance=user, data=data, partial=True)
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )            
        
        if 'password' in serializer.validated_data:
            message = 'Password modification is not allowed through this endpoint.'
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def delete(self, request, format=None):
        user = get_object_or_404(User, id=request.user.id)
        user.is_active = False
        user.save()
        return Response({'success:': 'User is inactive'}, status=status.HTTP_200_OK)

