from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import BusinessSerializer


class BusinessEndpoint(APIView):
    '''
    API view to manage authenticated owner's business data.
    '''    
    permission_classes = [permissions.IsAdminUser]

    def check_field_errors(self, request, check_missing=False) -> set | None:
        request_fields = set(request.data.keys())
        valid_fields = set(BusinessSerializer.Meta.fields)
        required_fields = set(BusinessSerializer.Meta.required)

        invalid_fields = request_fields - valid_fields
        if invalid_fields:
            return invalid_fields
        
        if check_missing:
            missing_fields = request_fields - required_fields
            if missing_fields:
                return missing_fields

        return None    

    def post(self, request):
        data = request.data
        if not data:
            return Response(
                {'error': 'No data provided for business creation.'},
                status=status.HTTP_400_BAD_REQUEST                
            )
        
        field_errors = self.check_field_errors(request, check_missing=True)
        if field_errors:
            return Response(
                {
                    'error': f'Invalid or missing required fields: {", ".join(field_errors)}',
                    'expected': BusinessSerializer.Meta.expected
                }, 
                status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BusinessSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )   

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)            


    def get(self, request):
        ...


    def patch(self, request):
        ...


    def delete(self, request):
        ...
