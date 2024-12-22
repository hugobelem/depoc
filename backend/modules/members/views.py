from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.shortcuts import get_object_or_404

from modules.members.models import Members, MembersCredentials
from .serializers import MemberSerializer


class MembersEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]

    def check_field_errors(self, request) -> set | None:
        request_fields = set(request.data.keys())
        valid_fields = set(MemberSerializer.Meta.fields)
        invalid_fields = request_fields - valid_fields
        if invalid_fields:
            return invalid_fields
        return None
    

    def post(self, request):
        try:
            owner = request.post
            owner.business         
        except:
            message = 'Owner does not have a registered business.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)  

        data = request.data
        if not data:
            message = 'No data provided for member creation.'
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)   
            
        field_errors = self.check_field_errors(request)
        if field_errors:
            message = f'Invalid fields: {", ".join(field_errors)}'
            expected_fields = MemberSerializer.Meta.fields
            return Response(
                {'error': message, 'expected': expected_fields}, 
                status=status.HTTP_400_BAD_REQUEST
            )      
        
        serializer = MemberSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )   
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)   
