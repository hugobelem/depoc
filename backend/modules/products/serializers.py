from rest_framework import serializers

from django.db import transaction

from .models import Product, ProductCategory, ProductCostHistory

from modules.inventory.models import Inventory, InventoryTransaction


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


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
    

    @transaction.atomic
    def create(self, validated_data):
        product = super().create(validated_data)

        inventory = Inventory.objects.create(product=product)

        if product.stock > 0:
            InventoryTransaction.objects.create(
                type='inbound',
                inventory=inventory,
                quantity=product.stock,
                unit_cost=product.cost_price,
                description='Initial inbound quantity.'
            )

        return product


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
