from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.apps import apps

from .models import Products, Category, CostHistory

User = get_user_model()
Business = apps.get_model('modules_business', 'Business')
BusinessProducts = apps.get_model('modules_business', 'BusinessProducts')
BusinessProductsCategories = apps.get_model(
    'modules_business', 
    'BusinessProductsCategories'
)


def assign_product_to_business(product, business):
    BusinessProducts.objects.create(
        product=product,
        business=business
    )

def assign_category_to_business(category, business):
    BusinessProductsCategories.objects.create(
        category=category,
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
        category = instance.category
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
                    'category': category.name if category else '',
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
        product = Products.objects.create(**validated_data)
        assign_product_to_business(product, business)

        return product
    

    def update(self, instance, validated_data):
        Products.objects.filter(id=instance.id).update(**validated_data)
        instance.refresh_from_db()
        
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'status']
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
                },
                'status': representation.pop('status'),
            },
        }
    

    def create(self, validated_data):
        business = self.context['business']
        category = Category.objects.create(**validated_data)
        assign_category_to_business(category, business)

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
                    'id': instance.product.id,
                    'name': instance.product.name,
                },
                'quatity': representation.pop('quatity'),
                'pricing': {
                    'costPrice': representation.pop('costPrice'),
                    'costAverage': representation.pop('costAverage'),
                    'retailPrice': representation.pop('retailPrice'),
                    'markup': representation.pop('markup'),
                },
                'effectiveDate': representation.pop('effectiveDate'),
            },
        }


    def create(self, validated_data):
        if 'markup' not in validated_data:
            validated_data['markup'] = self.context['markup']

        cost_history = CostHistory.objects.create(**validated_data)

        return cost_history
    

    def update(self, instance, validated_data):
        CostHistory.objects.filter(id=instance.id).update(**validated_data)
        instance.refresh_from_db()

        return instance