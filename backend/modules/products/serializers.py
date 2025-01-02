from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.apps import apps

import ulid
import json

from .models import Products, Category, CostHistory

User = get_user_model()
Business = apps.get_model('modules_business', 'Business')
BusinessProducts = apps.get_model('modules_business', 'BusinessProducts')


def assign_product_to_business(product, business):
    business_products_id = ulid.new().str
    BusinessProducts.objects.create(
        id=business_products_id,
        product=product,
        business=business
    )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'status',
            'name',
            'sku',
            'weight',
            'unit',
            'stock',
            'available',
            'trackStock',
            'brand',
            'origin',
            'ncm',
            'barcode',
            'cest',
            'category',
            'costPrice',
            'retailPrice',
            'discountedPrice',
        ]
        required = ['name']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'id': instance.id,
            'details': {
                'status': representation.pop('status'),
                'name': representation.pop('name'),
                'sku': representation.pop('sku'),
                'unit': representation.pop('unit'),
                'inventory': {
                    'stock': representation.pop('stock'),
                    'trackStock': representation.pop('trackStock'),
                    'available': representation.pop('available'),
                },
                'specifications': {
                    'weight': representation.pop('weight'),
                    'brand': representation.pop('brand'),
                    'category': representation.pop('category'),
                },
                'fiscal': {
                    'origin': representation.pop('origin'),
                    'ncm': representation.pop('ncm'),
                    'barcode': representation.pop('barcode'),
                    'cest': representation.pop('cest'),
                },
                'pricing':{
                    'costPrice': representation.pop('costPrice'),
                    'retailPrice': representation.pop('retailPrice'),
                    'discountedPrice': representation.pop('discountedPrice'),
                },
            },
        }


    def create(self, validated_data):
        business = self.context['business']

        product_id = ulid.new().str
        product = Products.objects.create(id=product_id, **validated_data)
        assign_product_to_business(product, business)

        return product
    

    def update(self, instance, validated_data):
        Products.objects.filter(id=instance.id).update(**validated_data)
        instance.refresh_from_db()
        
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'parent']
        required = ['name']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        parent = instance.parent
        return {
            'id': instance.id,
            'details': {
                'name': representation.pop('name'),
                'parent': {
                    'parentId': representation.pop('parent'),
                    'parentName': parent.name if parent else ''
                }
            },
        }
    

    def create(self, validated_data):
        category_id = ulid.new().str
        category = Category.objects.create(id=category_id, **validated_data)

        return category
    

    def update(self, instance, validated_data):
        Category.objects.filter(id=instance.id).update(**validated_data)
        instance.refresh_from_db()

        return instance


class CostHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CostHistory
        fields = [
            'product',
            'source',
            'quatity',
            'effectiveDate',
            'costPrice',
            'costAverage',
            'retailPrice',
            'markup',
        ]
        required = [field for field in fields if field != 'markup']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'id': instance.id,
            'details': {
                'product': {
                    'id': representation.pop('product_id'),
                    'name': representation.pop('product'),
                },
                'quatity': representation.pop('quatity'),
                'pricing': {
                    'costPrice': representation.pop('costPrice'),
                    'costAverage': representation.pop('costAverage'),
                    'retailPrice': representation.pop('retailPrice'),
                    'markup': representation.pop('markup'),
                },
                'effectiveDate': representation.pop('effectiveDate'),
                'source': representation.pop('source'),
            },
        }


    def create(self, validated_data):
        cost_history_id = ulid.new().str
        cost_history = CostHistory.objects.create(
            id=cost_history_id,
            **validated_data
        )

        return cost_history
    

    def update(self, instance, validated_data):
        CostHistory.objects.filter(id=instance.id).update(**validated_data)
        instance.refresh_from_db()

        return instance