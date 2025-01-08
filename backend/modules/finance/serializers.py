from rest_framework import serializers

from django.apps import apps

from .models import BankAccount

BusinessBankAccounts = apps.get_model('modules_business', 'BusinessBankAccounts')


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

    def create(self, validated_data):
        business = self.context['business']

        bank_account = BankAccount.objects.create(**validated_data)

        BusinessBankAccounts.objects.create(
            business=business,
            bankAccount=bank_account
        )

        return bank_account