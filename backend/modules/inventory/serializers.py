from rest_framework import serializers

from .models import Inventory, InventoryTransaction


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product = instance.product
        return {
            'id': instance.id,
            'details': {
                'product': {
                    'productId': product.id,
                    'productName': product.name,
                },
                'quantity': representation.pop('quantity'),
                'reserved': representation.pop('reserved'),
                'location': representation.pop('location'),
            },
        }
