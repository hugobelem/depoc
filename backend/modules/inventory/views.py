from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from . import services
from .throttling import BurstRateThrottle, SustainedRateThrottle
from .serializers import InventorySerializer, InventoryTransactionSerializer
from .models import InventoryTransaction

class InventoryEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def patch(self, request, product_id):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response

        business_products = services.get_business_products(business)
        if isinstance(business, Response):
            error_response = business_products
            return error_response
        
        data = services.get_data(request)
        if isinstance(business, Response):
            error_response = data
            return error_response
        
        if field_errors := services.check_field_errors(request, InventorySerializer):
            return field_errors
        
        inventory = services.get_inventory(product_id)
        if isinstance(inventory, Response):
            error_response = inventory
            return inventory

        serializer = InventorySerializer(instance=inventory, data=data, partial=True)

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, product_id=None):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        business_products = services.get_business_products(business)
        if isinstance(business, Response):
            error_response = business_products
            return error_response

        if product_id:
            inventory = services.get_inventory(product_id)
            if isinstance(inventory, Response):
                error_response = inventory
                return inventory
            serializer = InventorySerializer(inventory)
        else:
            products = [bp.product for bp in business_products]
            inventories = [product.inventory for product in products]
            serializer = InventorySerializer(inventories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class InventoryTransactionEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def post(self, request, product_id):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        business_products = services.get_business_products(business)
        if isinstance(business, Response):
            error_response = business_products
            return error_response
        
        data = services.get_data(request)
        if isinstance(business, Response):
            error_response = data
            return error_response
        
        if field_errors := services.check_field_errors(
            request,
            InventoryTransactionSerializer
        ):
            return field_errors
        
        inventory = services.get_inventory(product_id)
        if isinstance(inventory, Response):
                error_response = inventory
                return inventory

        data['inventory'] = inventory.id

        serializer = InventoryTransactionSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request, product_id, transaction_id=None):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        business_products = services.get_business_products(business)
        if isinstance(business, Response):
            error_response = business_products
            return error_response
        
        inventory = services.get_inventory(product_id)
        if isinstance(inventory, Response):
                error_response = inventory
                return inventory
        
        transactions = inventory.transactions.all()
        
        if transaction_id:
            transaction = services.get_transaction(transaction_id)

            if isinstance(transaction, Response):
                error_response = transaction
                return error_response
            
            serializer = InventoryTransactionSerializer(transaction)
        else:
            serializer = InventoryTransactionSerializer(transactions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
