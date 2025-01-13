from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q

from .models import Customer, Supplier
from .serializers import CustomerSerializer, SupplierSerializer

from shared import (
    error,
    validate,
    paginate,
    BurstRateThrottle,
    SustainedRateThrottle,
    get_user_business,
)


class ContactsSearchEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request):
        search = request.query_params.get('search', None)

        if not search:
            error_response = error.builder(400, 'Provide a search term.')
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        if len(search) < 3:
            error_response = error.builder(400, 'Enter at least 3 characters.')
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

        business, error_response = get_user_business(request.user)

        if error_response:
            return Response(error_response, status.HTTP_404_NOT_FOUND)

        search_customers = Customer.objects.filter(
            Q(business=business) &
            Q(code__icontains=search) |
            Q(name__icontains=search) |
            Q(alias__icontains=search) |
            Q(cpf__icontains=search)
        )

        search_suppliers = Supplier.objects.filter(
            Q(business=business) &
            Q(code__icontains=search) |
            Q(legal_name__icontains=search) |
            Q(trade_name__icontains=search) |
            Q(cnpj__icontains=search)
        )

        customers = CustomerSerializer(search_customers, many=True)
        suppliers = SupplierSerializer(search_suppliers, many=True)
        contacts = customers.data + suppliers.data

        paginated_data = paginate(contacts, request, 50)

        return paginated_data


class ContactsEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request):        
        business, error_response = get_user_business(request.user)

        if error_response:
            return Response(error_response, status.HTTP_404_NOT_FOUND)

        customers = CustomerSerializer(business.customers, many=True)
        suppliers = SupplierSerializer(business.suppliers, many=True)   
        contacts = customers.data + suppliers.data

        paginated_data = paginate(contacts, request, 50)
        
        return paginated_data


class CustomerEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, customer_id=None):
        business, error_response = get_user_business(request.user)

        if error_response:
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        if customer_id:
            customer = Customer.objects.filter(id=customer_id).first()
            if not customer:
                error_response = error.builder(404, 'Customer not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            serializer = CustomerSerializer(customer)
        else:
            customers = business.customers
            serializer = CustomerSerializer(customers, many=True)
            paginated_data = paginate(serializer.data, request, 50)
            return paginated_data

        return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request):
        data = request.data

        business, error_response = get_user_business(request.user)

        if error_response:
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        invalid_params = validate.params(request, CustomerSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

        serializer = CustomerSerializer(data=data, context={'business': business})
        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    def patch(self, request, customer_id):
        data = request.data

        business, error_response = get_user_business(request.user)

        if error_response:
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        invalid_params = validate.params(request, CustomerSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        customer = Customer.objects.filter(id=customer_id).first()
        if not customer:
            error_response = error.builder(404, 'Customer not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(instance=customer, data=data, partial=True)
        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request, customer_id):
        business, error_response = get_user_business(request.user)

        if error_response:
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        customer = Customer.objects.filter(id=customer_id).first()
        if not customer:
            error_response = error.builder(404, 'Customer not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        customer.is_active = False
        customer.save()

        data = {
            'customer': {
                'is_active': False
            }
        }

        return Response(data, status.HTTP_200_OK)


class SupplierEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, supplier_id=None):
        business, error_response = get_user_business(request.user)

        if error_response:
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        if supplier_id:
            supplier = Supplier.objects.filter(id=supplier_id).first()
            if not supplier:
                error_response = error.builder(404, 'Supplier not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            serializer = SupplierSerializer(supplier)
        else:
            suppliers = business.suppliers
            serializer = SupplierSerializer(suppliers, many=True)
            paginated_data = paginate(serializer.data, request, 50)
            return paginated_data

        return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request):
        data = request.data

        business, error_response = get_user_business(request.user)

        if error_response:
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        invalid_params = validate.params(request, SupplierSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)

        serializer = SupplierSerializer(data=data, context={'business': business})
        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    def patch(self, request, supplier_id):
        data = request.data

        business, error_response = get_user_business(request.user)

        if error_response:
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        invalid_params = validate.params(request, SupplierSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        supplier = Supplier.objects.filter(id=supplier_id).first()
        if not supplier:
            error_response = error.builder(404, 'Supplier not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)

        serializer = SupplierSerializer(instance=supplier, data=data, partial=True)
        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request, supplier_id):
        business, error_response = get_user_business(request.user)

        if error_response:
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        supplier = Supplier.objects.filter(id=supplier_id).first()
        if not supplier:
            error_response = error.builder(404, 'Supplier not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        supplier.is_active = False
        supplier.save()

        data = {
            'supplier': {
                'is_active': False
            }
        }

        return Response(data, status.HTTP_200_OK)
