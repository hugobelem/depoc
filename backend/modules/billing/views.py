from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q

from datetime import datetime

from .serializers import PaymentSerializer

from shared import (
    error,
    validate,
    paginate,
    BurstRateThrottle,
    SustainedRateThrottle,
    get_user_business,
    get_start_and_end_date
)


class ReceivableSearchEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        payments = business.payments.filter(payment_type='receivable')

        search = request.query_params.get('search')
        date = request.query_params.get('date')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not any([search, date, start_date, end_date]):
            message = 'Search term missing or invalid.'
            error_response = error.builder(400, message)
            return Response(error_response,status.HTTP_400_BAD_REQUEST)
        
        if search:
            if len(search) < 3:
                error_response = error.builder(400, 'Enter at least 3 characters.')
                return Response(error_response, status.HTTP_400_BAD_REQUEST)
            
            payments = payments.filter(
                Q(contact__customer__name__icontains=search) |
                Q(contact__supplier__legal_name__icontains=search) |
                Q(reference__icontains=search) |
                Q(notes__icontains=search)
            )

        if date:
            today = datetime.now()

            is_date_valid = validate.date(date, ignore=['today', 'week', 'month'])

            if not is_date_valid:
                message = 'Make sure the date is in the format: YYYY-MM-DD.'
                error_response = error.builder(400, message)
                return Response(error_response, status.HTTP_400_BAD_REQUEST)
            
            query = Q(due_at=date)

            if date == 'today':
                query = Q(due_at__exact=today)
            elif date == 'week':
                start_week, end_week = get_start_and_end_date(today, week=True)
                query = Q(due_at__range=[start_week, end_week])
            elif date == 'month':
                start_month, end_month = get_start_and_end_date(today, month=True)
                query = Q(due_at__range=[start_month, end_month])

            payments = payments.filter(query)

        if start_date and end_date:
            is_start_date_valid = validate.date(start_date)
            is_end_date_valid = validate.date(end_date)

            if not is_start_date_valid or not is_end_date_valid:
                message = 'Make sure the date is in the format: YYYY-MM-DD.'
                error_response = error.builder(400, message)
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            
            payments = payments.filter(
                Q(due_at__range=[start_date, end_date])
            )
   
        serializer = PaymentSerializer(payments, many=True)
        paginated_data = paginate(serializer.data, request, 10)

        return paginated_data


class ReceivablesEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, receivable_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        payments = business.payments.filter(payment_type='receivable')

        if receivable_id:
            payment = payments.filter(id=receivable_id).first()

            if not payment:
                error_response = error.builder(404, 'Receivable not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            serializer = PaymentSerializer(payments, many=True)
            paginated_data = paginate(serializer.data, request, 10)
            return paginated_data
        

    def post(self, request):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_paramns = validate.params(
            request,
            PaymentSerializer,
            remove=['payment_type'],
        )

        if not data or invalid_paramns:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_paramns)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        data['business'] = business.id
        data['payment_type'] = 'receivable'
        serializer = PaymentSerializer(data=data)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    def patch(self, request, receivable_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_paramns = validate.params(
            request,
            PaymentSerializer,
            remove=['payment_type'],
        )

        if not data or invalid_paramns:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_paramns)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        payments = business.payments
        payment = payments.filter(id=receivable_id).first()

        if not payment:
            error_response = error.builder(404, 'Receivable not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
            
        serializer = PaymentSerializer(instance=payment, data=data, partial=True)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request, receivable_id):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        payments = business.payments
        payment = payments.filter(id=receivable_id).first()

        if not payment:
            error_response = error.builder(404, 'Receivable not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        data = {
            'payment': {
                'id': payment.id,
                'deleted': True,
            }
        }

        payment.delete()

        return Response(data, status.HTTP_200_OK)


class ReceivableSettleEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def patch(self, request, receivable_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        remove = [
            'contact',
            'category',
            'issued_at',
            'due_at',
            'updated_at',
            'total_amount',
            'outstanding_balance',
            'payment_type',
            'status',
            'recurrence',
            'installment_count',
            'due_weekday',
            'due_day_of_month',
            'reference',
            'notes',
        ]

        invalid_paramns = validate.params(request, PaymentSerializer, remove=remove)

        if not data or invalid_paramns:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_paramns)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        payments = business.payments
        payment = payments.filter(id=receivable_id).first()

        if not payment:
            error_response = error.builder(404, 'Receivable not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
            
        serializer = PaymentSerializer(instance=payment, data=data, partial=True)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


class PayableSearchEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        payments = business.payments.filter(payment_type='payable')

        search = request.query_params.get('search')
        date = request.query_params.get('date')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not any([search, date, start_date, end_date]):
            message = 'Search term missing or invalid.'
            error_response = error.builder(400, message)
            return Response(error_response,status.HTTP_400_BAD_REQUEST)
        
        if search:
            if len(search) < 3:
                error_response = error.builder(400, 'Enter at least 3 characters.')
                return Response(error_response, status.HTTP_400_BAD_REQUEST)
            
            payments = payments.filter(
                Q(contact__customer__name__icontains=search) |
                Q(contact__supplier__legal_name__icontains=search) |
                Q(reference__icontains=search) |
                Q(notes__icontains=search)
            )

        if date:
            today = datetime.now()

            is_date_valid = validate.date(date, ignore=['today', 'week', 'month'])

            if not is_date_valid:
                message = 'Make sure the date is in the format: YYYY-MM-DD.'
                error_response = error.builder(400, message)
                return Response(error_response, status.HTTP_400_BAD_REQUEST)
            
            query = Q(due_at=date)

            if date == 'today':
                query = Q(due_at__exact=today)
            elif date == 'week':
                start_week, end_week = get_start_and_end_date(today, week=True)
                query = Q(due_at__range=[start_week, end_week])
            elif date == 'month':
                start_month, end_month = get_start_and_end_date(today, month=True)
                query = Q(due_at__range=[start_month, end_month])

            payments = payments.filter(query)

        if start_date and end_date:
            is_start_date_valid = validate.date(start_date)
            is_end_date_valid = validate.date(end_date)

            if not is_start_date_valid or not is_end_date_valid:
                message = 'Make sure the date is in the format: YYYY-MM-DD.'
                error_response = error.builder(400, message)
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            
            payments = payments.filter(
                Q(due_at__range=[start_date, end_date])
            )
   
        serializer = PaymentSerializer(payments, many=True)
        paginated_data = paginate(serializer.data, request, 10)

        return paginated_data


class PayablesEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, payable_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        payments = business.payments.filter(payment_type='payable')

        if payable_id:
            payment = payments.filter(id=payable_id).first()

            if not payment:
                error_response = error.builder(404, 'Payable not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            serializer = PaymentSerializer(payments, many=True)
            paginated_data = paginate(serializer.data, request, 10)
            return paginated_data
        

    def post(self, request):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_paramns = validate.params(
            request,
            PaymentSerializer,
            remove=['payment_type'],
        )

        if not data or invalid_paramns:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_paramns)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        data['business'] = business.id
        data['payment_type'] = 'payable'
        serializer = PaymentSerializer(data=data)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    def patch(self, request, payable_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_paramns = validate.params(
            request,
            PaymentSerializer,
            remove=['payment_type'],
        )

        if not data or invalid_paramns:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_paramns)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        payments = business.payments
        payment = payments.filter(id=payable_id).first()

        if not payment:
            error_response = error.builder(404, 'Payable not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
            
        serializer = PaymentSerializer(instance=payment, data=data, partial=True)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request, payable_id):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        payments = business.payments
        payment = payments.filter(id=payable_id).first()

        if not payment:
            error_response = error.builder(404, 'Payable not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        data = {
            'payment': {
                'id': payment.id,
                'deleted': True,
            }
        }

        payment.delete()

        return Response(data, status.HTTP_200_OK)
