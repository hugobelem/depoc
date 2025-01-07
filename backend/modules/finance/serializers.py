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
        expected_fields = [field for field in fields if field != 'createdAt']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'id': instance.id,
            'details': {
                **representation
            },
        }
