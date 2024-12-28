from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.apps import apps
from django.http import Http404

from .serializers import ContactsSerializer

BusinessOwner = apps.get_model('modules_business', 'BusinessOwner')
BusinessContacts = apps.get_model('modules_business', 'BusinessContacts')


def check_field_errors(request):
    request_fields = set(request.data.keys())
    valid_fields = set(ContactsSerializer.Meta.fields)
    invalid_fields = request_fields - valid_fields

    if invalid_fields:
        message = f'Invalid fields: {", ".join(invalid_fields)}'
        expected_fields = ContactsSerializer.Meta.fields
        return Response(
            {'error': message, 'expected': expected_fields}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return None


def get_business(request):
    try:
        owner = get_object_or_404(BusinessOwner, owner=request.user)
        business = owner.business
    except Http404:
        message = 'Owner does not have a registered business.'
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND) 
    
    if not business.active:
        message = 'The business is deactivated.'
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
    
    return business


def get_data(request):  
    data = request.data
    if not data:
        message = 'No data provided for contact creation or update.'
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)   
      
    return data


def get_business_contacts(business):
    business_contacts = BusinessContacts.objects.filter(business=business.id)
    if not business_contacts.exists():
        message = 'The business does not have registered contacts.'
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
    
    return business_contacts
