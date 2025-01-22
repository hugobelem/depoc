from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Q

from .utils.calculate import calculate_markup, calculate_average_cost

from .serializers import (
    ProductSerializer,
    ProductCategorySerializer,
    ProductCostHistorySerializer,
)

from shared import (
    error,
    validate,
    paginate,
    BurstRateThrottle,
    SustainedRateThrottle,
    get_user_business,
)


class ProductSearchEndpoint(APIView):
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

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_404_NOT_FOUND)
        
        products = business.products

        search_products = products.filter(
            Q(name__icontains=search) |
            Q(id__exact=search) |
            Q(sku__exact=search) |
            Q(barcode__exact=search)
        )

        serializer = ProductSerializer(search_products, many=True)
        paginated_data = paginate(serializer.data, request, 10)

        return paginated_data


class ProductEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, product_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        products = business.products

        if product_id:
            product = products.filter(id=product_id).first()

            if not product:
                error_response = error.builder(404, 'Product not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            
            serializer = ProductSerializer(product)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            serializer = ProductSerializer(products, many=True)
            paginated_data = paginate(serializer.data, request, 10)
            return paginated_data


    def post(self, request):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_params = validate.params(request, ProductSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        data['business'] = business.id
        serializer = ProductSerializer(data=data)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    def patch(self, request, product_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_params = validate.params(request, ProductSerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        products = business.products
        product = products.filter(id=product_id).first()
        if not product:
            error_response = error.builder(404, 'Product not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(instance=product, data=data, partial=True)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request, product_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        products = business.products
        product = products.filter(id=product_id).first()
        if not product:
            error_response = error.builder(404, 'Product not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        product.is_active = False
        product.is_available = False
        product.save()

        data = {
            'product': {
                'id': product.id,
                'is_active': False,
                'is_available': False,
            }
        }

        return Response(data, status.HTTP_200_OK)


class ProductCategoryEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, category_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        categories = business.product_categories

        if category_id:
            category = categories.filter(id=category_id).first()

            if not category:
                error_response = error.builder(404, 'Category not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            
            serializer = ProductCategorySerializer(category)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            serializer = ProductCategorySerializer(categories, many=True)
            paginated_data = paginate(serializer.data, request, 10)
            return paginated_data


    def post(self, request):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_params = validate.params(request, ProductCategorySerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        data['business'] = business.id
        serializer = ProductCategorySerializer(data=data)

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
        
        invalid_params = validate.params(request, ProductCategorySerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        categories = business.product_categories
        category = categories.filter(id=category_id).first()
        if not category:
            error_response = error.builder(404, 'Category not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)

        serializer = ProductCategorySerializer(
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
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
           
        categories = business.product_categories
        category = categories.filter(id=category_id).first()
        if not category:
            error_response = error.builder(404, 'Category not found.')
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


class ProductCostHistoryEndpoint(APIView):
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]

    def get(self, request, product_id, cost_id=None):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        products = business.products
        product = products.filter(id=product_id).first()
        if not product:
            error_response = error.builder(404, 'Product not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)

        costs = product.cost_history
        if cost_id:
            cost = costs.filter(id=cost_id).first()
            
            if not cost:
                error_response = error.builder(404, 'Cost not found.')
                return Response(error_response, status.HTTP_404_NOT_FOUND)
            
            serializer = ProductCostHistorySerializer(cost)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            serializer = ProductCostHistorySerializer(costs, many=True)
            paginated_data = paginate(serializer.data, request, 10)
            return paginated_data


    def post(self, request, product_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_params = validate.params(request, ProductCostHistorySerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        products = business.products
        product = products.filter(id=product_id).first()
        if not product:
            error_response = error.builder(404, 'Product not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)

        data['product'] = product.id

        # Automatically calculates the markup
        # if the user does not specify a value.
        markup = data.get('markup')
        if not markup:
            markup = calculate_markup(data)
            data['markup'] = markup

        # Automatically calculates the average cost
        # if the user does not specify a value.
        average_cost = data.get('average_cost')
        if not average_cost:
            average_cost = calculate_average_cost(data, business)
            data['average_cost'] = average_cost

        serializer = ProductCostHistorySerializer(data=data)

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    def patch(self, request, product_id, cost_id):
        data = request.data

        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        invalid_params = validate.params(request, ProductCostHistorySerializer)

        if not data or invalid_params:
            message = 'Required parameter missing or invalid.'
            error_response = error.builder(400, message, invalid=invalid_params)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        products = business.products
        product = products.filter(id=product_id).first()
        if not product:
            error_response = error.builder(404, 'Product not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        costs = product.cost_history
        cost = costs.filter(id=cost_id).first()
        if not cost:
            error_response = error.builder(404, 'Cost not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        serializer = ProductCostHistorySerializer(
            instance=cost,
            data=data,
            partial=True,
        )

        if not serializer.is_valid():
            message = 'Validation failed.'
            error_response = error.builder(400, message, details=serializer.errors)
            return Response(error_response, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


    def delete(self, request, product_id, cost_id):
        business, got_no_business = get_user_business(request.user)

        if got_no_business:
            return Response(got_no_business, status.HTTP_400_BAD_REQUEST)
        
        products = business.products
        product = products.filter(id=product_id).first()
        if not product:
            error_response = error.builder(404, 'Product not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
        
        costs = product.cost_history
        cost = costs.filter(id=cost_id).first()
        if not cost:
            error_response = error.builder(404, 'Cost not found.')
            return Response(error_response, status.HTTP_404_NOT_FOUND)
    
        data = {
            'cost': {
                'id': cost.id,
                'deleted': True,
            }
        }

        cost.delete()

        return Response(data, status.HTTP_200_OK)
