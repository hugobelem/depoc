from rest_framework import serializers

from .models import Inventory, InventoryTransaction


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
        read_only_fields = ['quantity', 'reserved', 'product']

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        inventory = instance
        product = inventory.product
        return {
            'inventory': {
                'id': representation.pop('id'),
                'quantity': representation.pop('quantity'),
                'reserved': representation.pop('reserved'),
                'location': representation.pop('location'),
                'product': {
                    'id': representation.pop('product'),
                    'name': product.name,
                },
            }
        }


class InventoryTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTransaction
        fields = '__all__'
        read_only_fields = ['date']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        transaction = instance
        inventory = transaction.inventory
        return {
            'transaction': {
                'id': representation.pop('id'),
                'type': representation.pop('type'),
                'date': representation.pop('date'),
                'quantity': representation.pop('quantity'),
                'unit_cost': representation.pop('unit_cost'),
                'unit_price': representation.pop('unit_price'),
                'description': representation.pop('description'),
                'inventory': {
                    'id': representation.pop('inventory'),
                    'product': inventory.product.name,
                },
            }
        }
