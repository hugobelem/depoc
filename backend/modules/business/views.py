from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import BusinessSerializer
from .models import Business, BusinessOwner # type: ignore


class BusinessEndpoint(APIView):
    '''
    API view to manage authenticated owner's business data.
    '''    
    permission_classes = [permissions.IsAdminUser]

    def check_field_errors(self, request) -> set | None:
        request_fields = set(request.data.keys())
        valid_fields = set(BusinessSerializer.Meta.fields)

        invalid_fields = request_fields - valid_fields
        if invalid_fields:
            return invalid_fields

        return None    


    def post(self, request):
        owner = request.user

        try:
            owner.business
            return Response(
                {'error': 'The owner is associated with an existing business.'},
                status=status.HTTP_400_BAD_REQUEST
            )                 
        except:
            pass

        data = request.data
        if not data:
            return Response(
                {'error': 'No data provided for business creation.'},
                status=status.HTTP_400_BAD_REQUEST                
            )
        
        field_errors = self.check_field_errors(request)
        if field_errors:
            return Response(
                {
                    'error': f'Invalid fields: {", ".join(field_errors)}',
                    'expected': BusinessSerializer.Meta.expected
                }, 
                status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BusinessSerializer(data=data, context={'owner': owner})
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )   

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)            


    def get(self, request):
        try:
            owner = get_object_or_404(BusinessOwner, owner=request.user)
            business = get_object_or_404(Business, id=owner.business.id)
            serializer = BusinessSerializer(business)            
        except:
            return Response(
                {'error': 'Owner does not have a registered business.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request):
        data = request.data

        try:
            owner = get_object_or_404(BusinessOwner, owner=request.user)
            business = get_object_or_404(Business, id=owner.business.id)
        except:
            return Response(
                {'error': 'Owner does not have a registered business.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not data:
            return Response(
                {'error': 'No data provided for business creation.'},
                status=status.HTTP_400_BAD_REQUEST                
            )
        
        field_errors = self.check_field_errors(request)
        if field_errors:
            return Response(
                {
                    'error': f'Invalid fields: {", ".join(field_errors)}',
                    'expected': BusinessSerializer.Meta.expected
                }, 
                status=status.HTTP_400_BAD_REQUEST)   
        
        serializer = BusinessSerializer(instance=business, data=data, partial=True)
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )           
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)         


    def delete(self, request):
        try:
            owner = get_object_or_404(BusinessOwner, owner=request.user)
            business = get_object_or_404(Business, id=owner.business.id)
        except:
            return Response(
                {'error': 'Owner does not have a registered business.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        business.active = False
        business.save()
        return Response(
            {'success:': 'The business has been successfully deactivated'},
            status=status.HTTP_200_OK
        )               
