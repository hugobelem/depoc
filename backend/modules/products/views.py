from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from . import services
from .throttling import BurstRateThrottle, SustainedRateThrottle
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    CostHistorySerializer
)
from .models import Category


class ProductsEndpoint(APIView):
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
        
        if field_errors := services.check_field_errors(request, ProductSerializer):
            return field_errors
        
        serializer = ProductSerializer(data=data, context={'business': business})
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )   
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def get(self, request, id=None):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        business_products = services.get_business_products(business)
        if isinstance(business_products, Response):
            error_response = business_products
            return error_response
        
        if id:
            products = business_products.filter(product__id=id).first()
            if not products:
                message = 'Product not found.'
                return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(products.product)
        else:
            products = [bp.product for bp in business_products]
            serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, id):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        data = services.get_data(request)
        if isinstance(data, Response):
            error_response = data
            return error_response
        
        if field_errors := services.check_field_errors(request, ProductSerializer):
            return field_errors
        
        business_products = services.get_business_products(business)
        if isinstance(business_products, Response):
            error_response = business_products
            return error_response
        
        products = business_products.filter(product__id=id).first()
        if not products:
            message = 'Product not found.'
            return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)

        product = products.product
        serializer = ProductSerializer(
            instance=product,
            data=data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, id):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        business_products = services.get_business_products(business)
        if isinstance(business_products, Response):
            error_response = business_products
            return error_response
        
        products = business_products.filter(product__id=id).first()
        if not products:
            message = 'Product not found.'
            return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)
        
        product = products.product
        if product.status == 'DELETED':
            message = 'Product already marked as deleted.'
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            product.status = 'DELETED'
            product.available = False
            product.save()
        
        return Response({'success': 'Product deleted'}, status=status.HTTP_200_OK)
    

class ProductCategoryEndpoint(APIView):
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
        
        if field_errors := services.check_field_errors(request, CategorySerializer):
            return field_errors
        
        serializer = CategorySerializer(data=data, context={'business': business})
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )   
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, id=None):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        categories = Category.objects.all()
        if not categories.exists():
            message = 'No product category was found.'
            return Response({'details': message}, status=status.HTTP_404_NOT_FOUND)
        
        if id:
            product = categories.filter(id=id).first()
            if not product:
                message = 'Category not found.'
                return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)
            serializer = CategorySerializer(product)
        else:
            serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, id):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        data = services.get_data(request)
        if isinstance(data, Response):
            error_response = data
            return error_response
        
        if field_errors := services.check_field_errors(request, CategorySerializer):
            return field_errors
        
        category = Category.objects.filter(id=id).first()
        if not category:
            message = 'Category not found.'
            return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(instance=category, data=data, partial=True)

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, id):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        category = Category.objects.filter(id=id).first()
        if not category:
            message = 'Category not found.'
            return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)
        
        if category.status == 'DELETED':
            message = 'Category already marked as deleted.'
            return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            category.status = 'DELETED'
            category.save()

        subcategories = category.subcategories.all()
        for sub in subcategories:
            sub.status = 'DELETED'
            sub.save()

        return Response({'success': 'Category deleted'}, status=status.HTTP_200_OK)
    

class ProductCostHistoryEndpoint(APIView):
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
            CostHistorySerializer
        ):
            return field_errors

        
        serializer = CostHistorySerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)