from rest_framework import serializers

from django.apps import apps

from .models import BankAccount, Category

BusinessBankAccounts = apps.get_model('modules_business', 'BusinessBankAccounts')
BusinessFinanceCategories = apps.get_model(
    'modules_business',
    'BusinessFinanceCategories'
)

def assign_category_to_business(category, business):
    BusinessFinanceCategories.objects.create(
        category=category,
        business=business
    )

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
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'status']
        expected_fields = ['name']


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
