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
from .models import Products, CostHistory


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
        
        product_categories = services.get_business_products_categories(business)
        if isinstance(product_categories, Response):
            error_response = product_categories
            return error_response
        
        categories = [product.category for product in product_categories]
        if id:
            selected_category = product_categories.filter(category__id=id).first()
            if not selected_category:
                message = 'Category not found.'
                return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)
            serializer = CategorySerializer(selected_category.category)
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
        
        product_categories = services.get_business_products_categories(business)
        if isinstance(product_categories, Response):
            error_response = product_categories
            return error_response
        
        selected_category = product_categories.filter(category__id=id).first()
        if not selected_category:
            message = 'Category not found.'
            return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)
        
        category = selected_category.category
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
        
        product_categories = services.get_business_products_categories(business)
        if isinstance(product_categories, Response):
            error_response = product_categories
            return error_response
        
        selected_category = product_categories.filter(category__id=id).first()
        if not selected_category:
            message = 'Category not found.'
            return Response({'error':message}, status=status.HTTP_404_NOT_FOUND)
        
        category = selected_category.category
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
        for categories in subcategories:
            categories.status = 'DELETED'
            categories.save()

        return Response({'success': 'Category deleted'}, status=status.HTTP_200_OK)
    

class ProductCostHistoryEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def post(self, request, product_id):
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
        
        data['product'] = product_id

        markup = services.calculate_markup(data)
        average_cost = services.calculate_average_cost(data)
        
        serializer = CostHistorySerializer(
            data=data,
            context={'markup': markup, 'average_cost': average_cost}
        )
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def get(self, request, product_id, cost_id=None):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        cost_histories = CostHistory.objects.filter(product__id=product_id)
        if not cost_histories.exists():
            message = 'No cost found for the specified product.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
        
        if cost_id:
            cost_history = cost_histories.filter(id=cost_id).first()
            if not cost_history:
                message = 'Cost History not found.'
                return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
            serializer = CostHistorySerializer(cost_history)
        else:
            serializer = CostHistorySerializer(cost_histories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, product_id, cost_id):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        cost_histories = CostHistory.objects.filter(product__id=product_id)
        if not cost_histories.exists():
            message = 'No cost found for the specified product.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
        
        cost_history = cost_histories.filter(id=cost_id).first()
        if not cost_history:
            message = 'Cost History not found.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
        
        data = services.get_data(request)
        if isinstance(data, Response):
            error_response = data
            return error_response
        
        data['product'] = product_id
        
        if field_errors := services.check_field_errors(
            request,
            CostHistorySerializer,
        ):
            return field_errors

        markup = services.calculate_markup(data)
        average_cost = services.calculate_average_cost(data)

        serializer = CostHistorySerializer(
            instance=cost_history,
            data=data,
            partial=True,
            context={'markup': markup, 'average_cost': average_cost},
        )

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, product_id, cost_id):
        business = services.get_business(request)
        if isinstance(business, Response):
            error_response = business
            return error_response
        
        product = Products.objects.filter(id=product_id).first()
        if not product:
            message = 'The specified product does not exists.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)    
        
        cost_histories = CostHistory.objects.filter(product__id=product_id)
        if not cost_histories.exists():
            message = 'The specified product does not have cost history.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
        
        cost_history = cost_histories.filter(id=cost_id).first()
        if not cost_history:
            message = 'Cost History not found.'
            return Response({'error': message}, status=status.HTTP_404_NOT_FOUND)
        
        cost_history.delete()

        return Response({'success': 'Cost deleted'}, status=status.HTTP_200_OK)
