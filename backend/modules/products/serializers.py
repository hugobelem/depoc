from rest_framework import serializers

from .models import Product, ProductCategory, ProductCostHistory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['stock']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product = instance
        category = product.category
        return {
            'product': {
                'id': representation.pop('id'),
                'name': representation.pop('name'),
                'sku': representation.pop('sku'),
                'barcode': representation.pop('barcode'),
                'brand': representation.pop('brand'),
                'category': category.name if category else None,
                'supplier': representation.pop('supplier'),
                'cost_price': representation.pop('cost_price'),
                'retail_price': representation.pop('retail_price'),
                'discounted_price': representation.pop('discounted_price'),
                'unit': representation.pop('unit'),
                'stock': representation.pop('stock'),
                'is_available': representation.pop('is_available'),
                'track_stock': representation.pop('track_stock'),
                'is_active': representation.pop('is_active'),
            }
        }


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'category': {
                'id': representation.pop('id'),
                'name': representation.pop('name'),
                'parent': representation.pop('parent'),
                'is_active': representation.pop('is_active'),
            }
        }


class ProductCostHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCostHistory
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'cost': {
                'id': representation.pop('id'),
                'effective_date': representation.pop('effective_date'),
                'quantity': representation.pop('quantity'),
                'cost_price': representation.pop('cost_price'),
                'average_cost': representation.pop('average_cost'),
                'retail_price': representation.pop('retail_price'),
                'markup': representation.pop('markup'),
                'product': representation.pop('product'),
            }
        }
