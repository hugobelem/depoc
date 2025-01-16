from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from decimal import Decimal, InvalidOperation

from .serializers import (
    FinancialAccountSerializer,
    FinancialCategorySerializer,
    FinancialTransactionSerializer,
)

from shared import (
    error,
    validate,
    paginate,
    IsOwner,
    BurstRateThrottle,
    SustainedRateThrottle,
    get_user_business,
)


class FinancialAccountEndpoint(APIView):
    permission_classes = [IsOwner]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, account_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        accounts = business.financial_accounts
        if account_id:
            account = accounts.filter(id=account_id).first()
            if not account:
                error_response = error.builder(404, 'Financial account not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            serializer = FinancialAccountSerializer(account)
        else:
            serializer = FinancialAccountSerializer(accounts, many=True)
            paginated_data = paginate(serializer.data, request, 10)
            return paginated_data

        return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)

        invalid_params = validate.params(request, FinancialAccountSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        data['business'] = business.id
        serializer = FinancialAccountSerializer(data=data)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    def patch(self, request, account_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)

        invalid_params = validate.params(request, FinancialAccountSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        accounts = business.financial_accounts
        account = accounts.filter(id=account_id).first()
        if not account:
            error_response = error.builder(404, 'Financial account not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        data['business'] = business.id
        serializer = FinancialAccountSerializer(
            instance=account,
            data=data,
            partial=True,
        )

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request, account_id):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)

        accounts = business.financial_accounts
        account = accounts.filter(id=account_id).first()
        if not account:
            error_response = error.builder(404, 'Financial account not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        account.is_active = False
        account.save()

        data = {
            'account': {
                'id': account.id,
                'is_active': False,
            }
        }

        return Response(data, status.HTTP_200_OK)


class FinancialCategoryEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, category_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        categories = business.financial_categories
        if category_id:
            category = categories.filter(id=category_id).first()
            if not category:
                error_response = error.builder(404, 'Financial category not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            serializer = FinancialCategorySerializer(category)
        else:
            serializer = FinancialCategorySerializer(categories, many=True)
            paginated_data = paginate(serializer.data, request, 10)
            return paginated_data

        return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)

        invalid_params = validate.params(request, FinancialCategorySerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        data['business'] = business.id
        serializer = FinancialCategorySerializer(data=data)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    def patch(self, request, category_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)

        invalid_params = validate.params(request, FinancialCategorySerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        categories = business.financial_categories
        category = categories.filter(id=category_id).first()
        if not category:
            error_response = error.builder(404, 'Financial category not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        data['business'] = business.id
        serializer = FinancialCategorySerializer(
            instance=category,
            data=data,
            partial=True,
        )

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request, category_id):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)

        categories = business.financial_categories
        category = categories.filter(id=category_id).first()
        if not category:
            error_response = error.builder(404, 'Financial category not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        category.is_active = False
        category.save()

        data = {
            'category': {
                'id': category.id,
                'is_active': False,
            }
        }

        return Response(data, status.HTTP_200_OK)


class FinancialTransactionEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, transaction_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        transactions = business.financial_transactions
        if transaction_id:
            transaction = transactions.filter(id=transaction_id).first()
            if not transaction:
                message = 'Financial transaction not found.'
                error_response = error.builder(404, message)
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            serializer = FinancialTransactionSerializer(transaction)
        else:
            serializer = FinancialTransactionSerializer(transactions, many=True)
            paginated_data = paginate(serializer.data, request, 10)
            return paginated_data

        return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request):
        data = request.data
        user = request.user

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)

        invalid_params = validate.params(
            request,
            FinancialTransactionSerializer,
            add='send_to',
        )

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

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

        data['business'] = business.id
        data['operator'] = user.id

        serializer = FinancialTransactionSerializer(
            data=data,
            context={'business': business, 'data': data, 'request': request},
        )

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    # def patch(self, request, transaction_id):
    #     data = request.data

    #     business, got_no_business = get_user_business(request.user)

    #     if got_no_business:
    #         return Response(got_no_business, status.HTTP_400_BAD_REQUEST)

    #     invalid_params = validate.params(request, FinancialTransactionSerializer)

    #     if not data or invalid_params:
    #         message = 'Required parameter missing or invalid.'
    #         error_response = error.builder(400, message, invalid=invalid_params)
    #         return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
    #     transactions = business.financial_transactions
    #     transaction = transactions.filter(id=transaction_id).first()
    #     if not transaction:
    #         error_response = error.builder(404, 'Transaction not found.')
    #         return Response(error_response, status.HTTP_404_NOT_FOUND)
        
    #     data['business'] = business.id
    #     serializer = FinancialTransactionSerializer(
    #         instance=transaction,
    #         data=data,
    #         partial=True,
    #     )

    #     if not serializer.is_valid():
    #         message = 'Validation failed.'
    #         error_response = error.builder(400, message, details=serializer.errors)
    #         return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
    #     serializer.save()

    #     return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request, transaction_id):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)

        transactions = business.financial_transactions
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
