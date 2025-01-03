from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.apps import apps
from django.http import Http404

from .serializers import ProductSerializer

BusinessOwner = apps.get_model('modules_business', 'BusinessOwner')
BusinessProducts = apps.get_model('modules_business', 'BusinessProducts')
BusinessProductsCategories = apps.get_model(
    'modules_business',
    'BusinessProductsCategories'
)


def check_field_errors(request, serializer):
    request_fields = set(request.data.keys())
    valid_fields = set(serializer.Meta.fields)
    invalid_fields = request_fields - valid_fields

    if invalid_fields:
        message = f'Invalid fields: {", ".join(invalid_fields)}'
        expected_fields = serializer.Meta.fields
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
        message = 'No data provided for product creation or update.'
        return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)   
      
    return data


def get_business_products(business):
    business_products = BusinessProducts.objects.filter(business=business.id)
    if not business_products.exists():
        message = 'The business does not have registered products.'
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
    
    return business_products


def get_business_products_categories(business):
    bp_categories = BusinessProductsCategories.objects.filter(business=business.id)
    if not bp_categories.exists():
        message = 'No product category was found.'
        return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
    
    return bp_categories
