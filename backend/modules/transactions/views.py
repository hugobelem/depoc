from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from . import services
from .throttling import BurstRateThrottle, SustainedRateThrottle
from .serializers import TransactionSerializer
from .models import Transaction

from decimal import Decimal, InvalidOperation


class TransactionEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def post(self, request):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        data = services.get_data(request)
        if isinstance(data, Response):
            error_response = data
            return error_response
        
        if field_errors := services.check_field_errors(
                request,
                TransactionSerializer,
            ):
            return field_errors
        
        if amount := data.get('amount', None):
            try:
                amount_cleaned = abs(Decimal(amount))
            except InvalidOperation:
                raise ValueError('Invalid monetary value format.')

        transaction_type = data.get('type', None)
        if transaction_type == 'credit':
            data['amount'] = amount_cleaned
        elif transaction_type == 'debit':
            data['amount'] = -amount_cleaned
        elif transaction_type == 'transfer':
            data['amount'] = -amount_cleaned

        serializer = TransactionSerializer(
            data=data,
            context={'business': business, 'data': data, 'request': request},
        )

        if not serializer.is_valid():
            message = 'Validation failed: '
            return Response(
                {'error': message, 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request, id=None):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        transactions = business.transactions

        if id:
            transaction = transactions.filter(id=id).first()
            serializer = TransactionSerializer(transaction)
        else:
            serializer = TransactionSerializer(transactions, many=True)

        return Response(serializer.data)


    def patch(self, request, id):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        data = services.get_data(request)
        if isinstance(data, Response):
            error_response = data
            return error_response
        
        if field_errors := services.check_field_errors(
                request,
                TransactionSerializer,
            ):
            return field_errors
    
        transactions = business.transactions
        transaction = transactions.filter(id=id).first()

        serializer = TransactionSerializer(
            instance=transaction,
            data=data,
            partial=True
        )

        if not serializer.is_valid():
            message = 'Validation failed: '
            return Response(
                {'error': message, 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, id):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        transactions = business.transactions
        transaction = transactions.filter(id=id).first()

        transaction.delete()

        return Response({'sucess': 'Transaction deleted.'}, status.HTTP_200_OK)
