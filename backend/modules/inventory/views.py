from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import InventorySerializer, InventoryTransactionSerializer

from .models import Inventory, InventoryTransaction

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

    def get(self, request, inventory_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        fetch_inventory = Inventory.objects.filter(product__business=business)
        if inventory_id:
            inventory = fetch_inventory.filter(id=inventory_id).first()

            if not inventory:
                error_response = error.builder(404, 'Inventory not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)

            serializer = InventorySerializer(inventory)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            serializer = InventorySerializer(fetch_inventory, many=True)
            paginated_data = paginate(serializer.data, request, 50)
            return paginated_data


    def patch(self, request, inventory_id):
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
        
        fetch_inventory = Inventory.objects.filter(product__business=business)
        inventory = fetch_inventory.filter(id=inventory_id).first()
        
        if not inventory:
            error_response = error.builder(404, 'Inventory not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        serializer = InventorySerializer(
            instance=inventory,
            data=data,
            partial=True,
        )

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


class InventoryTransactionEndpoint(APIView):
    permission_classes = [IsOwner]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, inventory_id=None, transaction_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        fetch_inventory = Inventory.objects.filter(product__business=business)

        if inventory_id:
            inventory = fetch_inventory.filter(id=inventory_id).first()
            transactions = InventoryTransaction.objects.filter(inventory=inventory)
            if not inventory:
                error_response = error.builder(404, 'Inventory not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)

        if transaction_id:
            transactions = InventoryTransaction.objects.filter(
                inventory__product__business=business
            )
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


    def post(self, request, inventory_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_params = validate.params(request, InventoryTransactionSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        fetch_inventory = Inventory.objects.filter(product__business=business)
        inventory = fetch_inventory.filter(id=inventory_id).first()
        if not inventory:
            error_response = error.builder(404, 'Inventory not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        post_data = data.copy()

        if not post_data.get('quantity'):
            error_response = error.builder(404, 'Inform a quantity.')
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

        quantity_cleaned = abs(int(post_data.get('quantity')))

        transaction_type = post_data.get('type')
        if transaction_type == 'inbound':
            post_data['quantity'] = quantity_cleaned
        elif transaction_type == 'outbound':
            post_data['quantity'] = -quantity_cleaned
        
        post_data['inventory'] = inventory.id

        serializer = InventoryTransactionSerializer(data=post_data)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    def patch(self, request, transaction_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        remove = ['type', 'date']
        invalid_params = validate.params(
            request, InventoryTransactionSerializer, remove=remove
        )

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        transactions = InventoryTransaction.objects.filter(
            inventory__product__business=business
        )
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


    def delete(self, request, transaction_id):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        transactions = InventoryTransaction.objects.filter(
            inventory__product__business=business
        )
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
