from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q
from django.utils import timezone

from decimal import Decimal, InvalidOperation

from datetime import datetime

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
    get_start_and_end_date
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
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            serializer = FinancialAccountSerializer(accounts, many=True)
            paginated_data = paginate(serializer.data, request, 50)
            return paginated_data


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
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            serializer = FinancialCategorySerializer(categories, many=True)
            paginated_data = paginate(serializer.data, request, 50)
            return paginated_data


    def post(self, request):
        data = request.data
        post_data = data.copy()

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)

        invalid_params = validate.params(request, FinancialCategorySerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        post_data['business'] = business.id
        serializer = FinancialCategorySerializer(data=post_data)

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
        
        transactions = business.financial_transactions.order_by('-timestamp')
        if transaction_id:
            transaction = transactions.filter(id=transaction_id).first()
            
            if not transaction:
                message = 'Financial transaction not found.'
                error_response = error.builder(404, message)
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            
            serializer = FinancialTransactionSerializer(transaction)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            serializer = FinancialTransactionSerializer(transactions, many=True)
            paginated_data = paginate(serializer.data, request, 50)
            return paginated_data


    def post(self, request):
        data = request.data
        post_data = data.copy()
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
            post_data['amount'] = amount_cleaned
        elif transaction_type == 'debit':
            post_data['amount'] = -amount_cleaned
        elif transaction_type == 'transfer':
            post_data['amount'] = -amount_cleaned
            send_to = data.get('send_to', None)
            if not send_to:
                message = 'Destination account not provided'
                error_response = error.builder(400, message)
                return Response(error_response, status.HTTP_400_BAD_REQUEST)

        post_data['business'] = business.id
        post_data['operator'] = user.id

        serializer = FinancialTransactionSerializer(
            data=post_data,
            context={'business': business, 'data': post_data, 'request': request},
        )

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


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


class FinancialTransactionSearchEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_404_NOT_FOUND)
        
        search = request.query_params.get('search')
        date = request.query_params.get('date')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not any([search, date, start_date, end_date]):
            error_response = error.builder(400, 'Provide a search term or date.')
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        transactions = business.financial_transactions

        if search:
            if len(search) < 3:
                error_response = error.builder(400, 'Enter at least 3 characters.')
                return Response(error_response, status.HTTP_400_BAD_REQUEST)
            
            transactions = transactions.filter(
                Q(amount__startswith=search) |
                Q(description__icontains=search)
            )
        
        if date:
            today = datetime.now()

            is_date_valid = validate.date(date, ignore=['today', 'week', 'month'])

            if not is_date_valid:
                message = 'Make sure the date is in the format: YYYY-MM-DD.'
                error_response = error.builder(400, message)
                return Response(error_response, status.HTTP_400_BAD_REQUEST)
            
            query = Q(timestamp__date=date)

            if date == 'today':
                query = Q(timestamp__date=today)
            elif date == 'week':
                start_week, end_week = get_start_and_end_date(today, week=True)
                query = Q(timestamp__range=[start_week, end_week])
            elif date == 'month':
                start_month, end_month = get_start_and_end_date(today, month=True)
                query = Q(timestamp__range=[start_month, end_month])

            transactions = transactions.filter(query)

        if start_date and end_date:
            is_start_date_valid = validate.date(start_date)
            is_end_date_valid = validate.date(end_date)

            if not is_start_date_valid or not is_end_date_valid:
                message = 'Make sure the date is in the format: YYYY-MM-DD.'
                error_response = error.builder(400, message)
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            
            date_format = '%Y-%m-%d'
            start_date = datetime.strptime(start_date, date_format)
            end_date = datetime.strptime(end_date, date_format)

            start_date = timezone.make_aware(
                start_date.replace(hour=0, minute=0, second=0, microsecond=0),
                timezone.get_current_timezone(),
            )
            end_date = timezone.make_aware(
                end_date.replace(hour=23, minute=59, second=59, microsecond=0),
                timezone.get_current_timezone(),
            )

            transactions = transactions.filter(
                Q(timestamp__range=[start_date, end_date])
            )

        serializer = FinancialTransactionSerializer(transactions, many=True)
        paginated_data = paginate(serializer.data, request, 50)

        return paginated_data
