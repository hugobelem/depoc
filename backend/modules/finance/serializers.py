from rest_framework import serializers

from .models import BankAccount

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = [
            'bankName',
            'branchCode',
            'accountNumber',
            'balance',
            'createdAt',
            'status',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'id': instance.id,
            'details': {
                representation
            },
        }
