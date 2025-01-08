from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from . import services
from .throttling import BurstRateThrottle, SustainedRateThrottle
from .serializers import BankAccountSerializer


class BankAccountEndpoint(APIView):
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
                BankAccountSerializer,
            ):
            return field_errors
        
        serializer = BankAccountSerializer(
            data=data,
            context={'business': business},
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
        
        business_banks = services.get_business_banks(business)
        
        if id:
            bank_account = business_banks.filter(bankAccount__id=id).first()
            if not bank_account:
                message = 'Bank Account not found.'
                return Response({'error': message}, status.HTTP_404_NOT_FOUND)
            serializer = BankAccountSerializer(bank_account.bankAccount)
        else:
            bank_accounts = [business.bankAccount for business in business_banks]
            serializer = BankAccountSerializer(bank_accounts, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


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
                BankAccountSerializer,
            ):
            return field_errors
        
        business_banks = services.get_business_banks(business)

        bank_account = business_banks.filter(bankAccount__id=id).first()
        if not bank_account:
            message = 'Bank Account not found.'
            return Response({'error': message}, status.HTTP_404_NOT_FOUND)

        serializer = BankAccountSerializer(
            instance=bank_account.bankAccount,
            data=data,
            partial=True,
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
        
        business_banks = services.get_business_banks(business)

        get_bank_account = business_banks.filter(bankAccount__id=id).first()
        if not get_bank_account:
            message = 'Bank Account not found.'
            return Response({'error': message}, status.HTTP_404_NOT_FOUND)
        
        bank_account = get_bank_account.bankAccount
        bank_account.status = 'DELETED'
        bank_account.save()

        return Response({'success': 'Bank Account deleted.'}, status.HTTP_200_OK)
