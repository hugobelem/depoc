from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, throttling
from rest_framework import status

from django.shortcuts import get_object_or_404

from modules.business.models import Business, BusinessOwner
from .serializers import BusinessSerializer


class BusinessEndpoint(APIView): 
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [throttling.UserRateThrottle]

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
            message = 'The owner is associated with an existing business.'
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)                 
        except:
            pass

        data = request.data
        if not data:
            message = 'No data provided for business creation.'
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)   
            
        field_errors = self.check_field_errors(request)
        if field_errors:
            message = f'Invalid fields: {", ".join(field_errors)}'
            expected_fields = BusinessSerializer.Meta.expected
            return Response(
                {'error': message, 'expected': expected_fields}, 
                status=status.HTTP_400_BAD_REQUEST
            )      
        
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
            message = 'Owner does not have a registered business.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)  
             
        if not business.active:
            message = 'The business is deactivated.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)                  
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request):
        data = request.data
        try:
            owner = get_object_or_404(BusinessOwner, owner=request.user)
            business = get_object_or_404(Business, id=owner.business.id)
        except:
            message = 'Owner does not have a registered business.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
         
        if not business.active:
            message = 'The business is deactivated.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)  
                      
        if not data:
            message = 'No data provided for business creation.'
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
             
        field_errors = self.check_field_errors(request)
        if field_errors:
            message = f'Invalid fields: {", ".join(field_errors)}'
            expected_fields = BusinessSerializer.Meta.expected
            return Response(
                {'error': message, 'expected': expected_fields}, 
                status=status.HTTP_400_BAD_REQUEST
            )
               
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
            message = 'Owner does not have a registered business.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
        
        if not business.active:
            message = 'The business is already inactive.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
        
        business.active = False
        business.save()
        message = 'The business has been successfully deactivated'
        return Response({'success:': message}, status=status.HTTP_200_OK)
