from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.apps import apps
from django.http import Http404

from .models import Transaction

BusinessOwner = apps.get_model('modules_business', 'BusinessOwner')
BusinessProducts = apps.get_model('modules_business', 'BusinessProducts')
BusinessBankAccounts = apps.get_model('modules_business', 'BusinessBankAccounts')


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
        message = 'No data provided for resource creation or update.'
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)   
      
    return data


def check_field_errors(request, serializer):
    request_fields = set(request.data.keys())
    valid_fields = set(serializer.Meta.fields)
    valid_fields.add('sendTo')
    invalid_fields = request_fields - valid_fields

    if invalid_fields:
        message = f'Invalid fields: {", ".join(invalid_fields)}'
        expected_fields = serializer.Meta.expected_fields
        return Response(
            {'error': message, 'expected': expected_fields}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return None


def get_business_banks(business):
    business_banks = BusinessBankAccounts.objects.filter(business=business)
    if not business_banks:
        message = 'No bank found.'
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
    
    return business_banks


def complete_transfer(business, data, request, transaction):
    sendTo = data.get('sendTo', None)
    amount = data.get('amount', None)

    if sendTo:
        business_banks = get_business_banks(business)
        send_to = business_banks.filter(bankAccount__id=sendTo).first()
    
    Transaction.objects.create(
        amount=abs(amount),
        description='Transfer',
        type='transfer',
        bankAccount=send_to.bankAccount,
        createdBy=request.user,
        linkedTransaction=transaction
    )
