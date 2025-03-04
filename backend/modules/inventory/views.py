from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import InventorySerializer, InventoryTransactionSerializer

from shared import (
    error,
    validate,
    paginate,
    IsOwner,
    BurstRateThrottle,
    SustainedRateThrottle,
    get_user_business,
)


class InventoryEndpoint(APIView):
    permission_classes = [IsOwner]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, product_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        products = business.products.all()
        if product_id:
            product = products.filter(id=product_id).first()
            
            if not product:
                error_response = error.builder(404, 'Product not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            
            inventory = product.inventory
            serializer = InventorySerializer(inventory)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            all_inventory = [product.inventory for product in products]
            serializer = InventorySerializer(all_inventory, many=True)
            paginated_data = paginate(serializer.data, request, 50)
            return paginated_data


    def patch(self, request, product_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        lst = ['quantity', 'reserved', 'product']
        invalid_params = validate.params(request, InventorySerializer, remove=lst)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        products = business.products
        product = products.filter(id=product_id).first()
        if not product:
            error_response = error.builder(404, 'Product not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        inventory = product.inventory
        
        serializer = InventorySerializer(instance=inventory, data=data, partial=True)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


class InventoryTransactionEndpoint(APIView):
    permission_classes = [IsOwner]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, product_id, transaction_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        products = business.products
        product = products.filter(id=product_id).first()
        if not product:
            error_response = error.builder(404, 'Product not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        inventory = product.inventory
        transactions = inventory.transactions

        if transaction_id:
            transaction = transactions.filter(id=transaction_id).first()

            if not transaction:
                error_response = error.builder(404, 'Transaction not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            
            serializer = InventoryTransactionSerializer(transaction)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            serializer = InventoryTransactionSerializer(transactions, many=True)
            paginated_data = paginate(serializer.data, request, 50)
            return paginated_data


    def post(self, request, product_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_params = validate.params(request, InventoryTransactionSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        products = business.products
        product = products.filter(id=product_id).first()
        if not product:
            error_response = error.builder(404, 'Product not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        if quantity := data.get('quantity', None):
            quantity_cleaned = abs(quantity)

        transaction_type = data.get('type', None)
        if transaction_type == 'inbound':
            data['quantity'] = quantity_cleaned
        elif transaction_type == 'outbound':
            data['quantity'] = -quantity_cleaned
        elif transaction_type == 'balance':
            data['quantity'] = quantity_cleaned
        
        inventory = product.inventory
        data['inventory'] = inventory.id

        serializer = InventoryTransactionSerializer(data=data)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    def patch(self, request, product_id, transaction_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_params = validate.params(request, InventoryTransactionSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        products = business.products
        product = products.filter(id=product_id).first()
        if not product:
            error_response = error.builder(404, 'Product not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        inventory = product.inventory

        transactions = inventory.transactions
        transaction = transactions.filter(id=transaction_id).first()
        if not transaction:
            error_response = error.builder(404, 'Transaction not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        serializer = InventoryTransactionSerializer(
            instance=transaction,
            data=data,
            partial=True,
        )

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request, product_id, transaction_id):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        products = business.products
        product = products.filter(id=product_id).first()
        if not product:
            error_response = error.builder(404, 'Product not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        inventory = product.inventory

        transactions = inventory.transactions
        transaction = transactions.filter(id=transaction_id).first()
        if not transaction:
            error_response = error.builder(404, 'Transaction not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        data = {
            'transaction': {
                'id': transaction.id,
                'deleted': True,
            }
        }

        transaction.delete()

        return Response(data, status.HTTP_200_OK)
