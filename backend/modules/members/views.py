from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.apps import apps
from django.http import Http404

from .throttling import BurstRateThrottle, SustainedRateThrottle
from .serializers import MemberSerializer

Business = apps.get_model('modules_business', 'Business')
BusinessOwner = apps.get_model('modules_business', 'BusinessOwner')
BusinessMembers = apps.get_model('modules_business', 'BusinessMembers')


class MembersEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def check_field_errors(self, request) -> set | None:
        request_fields = set(request.data.keys())
        valid_fields = set(MemberSerializer.Meta.fields)
        invalid_fields = request_fields - valid_fields
        if invalid_fields:
            return invalid_fields
        return None
    

    def post(self, request):
        try:
            owner = get_object_or_404(BusinessOwner, owner=request.user)
            business = owner.business
        except Http404:
            message = 'Owner does not have a registered business.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND) 
        
        if not business.active:
            message = 'The business is deactivated.'
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
        
        serializer = MemberSerializer(data=data, context={'business': business})
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )   
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)   


    def get(self, request, id=None):
        try:
            owner = get_object_or_404(BusinessOwner, owner=request.user)
            business = owner.business
        except Http404:
            message = 'Owner does not have a registered business.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND) 
        
        if not business.active:
            message = 'The business is deactivated.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)

        business_members = BusinessMembers.objects.filter(business=business.id)
        if not business_members.exists():
            message = 'The business does not have registered members.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)

        if id:
            members = business_members.filter(member__id=id).first()
            if not members:
                message = 'Member not found.'
                return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
            serializer = MemberSerializer(members.member)
        else:
            members = [bm.member for bm in business_members]
            serializer = MemberSerializer(members, many=True)            
                              
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, id):
        try:
            owner = request.user
            get_owner = get_object_or_404(BusinessOwner, owner=owner)
            business = get_object_or_404(Business, id=get_owner.business.id)              
        except:
            message = 'Owner does not have a registered business.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)  
        
        if not business.active:
            message = 'The business is deactivated.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
        
        business_members = BusinessMembers.objects.filter(business=business.id)
        if not business_members:
            message = 'The business does not have registered members.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)  

        data = request.data
        if not data:
            message = 'No data provided for member update.'
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        
        members = business_members.filter(member__id=id).first()
        if not members:
            message = 'Member not found.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)       
        
        field_errors = self.check_field_errors(request)
        if field_errors:
            message = f'Invalid fields: {", ".join(field_errors)}'
            expected_fields = MemberSerializer.Meta.fields
            return Response(
                {'error': message, 'expected': expected_fields}, 
                status=status.HTTP_400_BAD_REQUEST
            )
         
        serializer = MemberSerializer(
            instance=members.member, 
            data=data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, id):
        try:
            owner = request.user
            get_owner = get_object_or_404(BusinessOwner, owner=owner)
            business = get_object_or_404(Business, id=get_owner.business.id)              
        except:
            message = 'Owner does not have a registered business.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)  
        
        if not business.active:
            message = 'The business is deactivated.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND) 

        business_members = BusinessMembers.objects.filter(business=business.id)
        if not business_members:
            message = 'The business does not have registered members.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)        
        
        members = business_members.filter(member__id=id).first()
        member = members.member
        if not members:
            message = 'Member not found.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND) 

        member.status = 'DELETED'
        member.save()
        message = 'The member has been successfully deleted'
        return Response({'success:': message}, status=status.HTTP_200_OK)
