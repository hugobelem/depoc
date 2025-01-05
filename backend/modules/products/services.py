from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.apps import apps
from django.http import Http404

from decimal import Decimal, InvalidOperation

from .models import Products

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
        valid_fields.discard('product')
        expected_fields = valid_fields
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


def calculate_markup(data):
    try:
        cost_price = Decimal(data.get('costPrice', 0))
        retail_price = Decimal(data.get('retailPrice', 0))

        if cost_price > 0 and retail_price > 0:
            markup = ((retail_price - cost_price) / cost_price) * 100
            return round(markup, 2)
    except (InvalidOperation, ValueError, TypeError):
        pass
    
    return None


def calculate_average_cost(data):
    product_quantity = data.get('quantity', 0)
    product_cost = data.get('costPrice', 0)
    product_id = data.get('product', '')
    
    product_total_cost = product_cost * product_quantity

    product = Products.objects.filter(id=product_id).first()
    if not product:
        return 0

    cost_history = product.cost_history.all()

    total_cost = product_total_cost
    total_quantity = product_quantity

    for history in cost_history:
        total_cost += history.costPrice * history.quantity
        total_quantity += history.quantity

    if total_quantity == 0:
        return 0
    
    return round(total_cost / total_quantity, 2)
