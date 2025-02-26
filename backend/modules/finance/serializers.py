from rest_framework import serializers

from django.db import transaction

from .models import FinancialAccount, FinancialCategory, FinancialTransaction


def complete_transfer(business, data, request, transaction):
    send_to = data.get('send_to', None)
    amount = data.get('amount', None)

    financial_accounts = business.financial_accounts
    destination_account = financial_accounts.filter(id=send_to).first()

    operator_description = data.get('description', None)
    transfer_description = f'Transfer Received from {transaction.account}'
    description = f'{transfer_description} • {operator_description}'
    
    if destination_account:
        transfer = FinancialTransaction.objects.create(
            type='transfer',
            operator=request.user,
            business=business,
            account=destination_account,
            linked=transaction,
            amount=abs(amount),
            description=description
        )

        return transfer

    return None


class FinancialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialAccount
        fields = '__all__'

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'account': {
                'id': representation.pop('id'),
                'name': representation.pop('name'),
                'balance': representation.pop('balance'),
                'created_at': representation.pop('created_at'),
                'is_active': representation.pop('is_active'),
            }
        }


class FinancialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialCategory
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'category': {
                'id': representation.pop('id'),
                'name': representation.pop('name'),
                'is_active': representation.pop('is_active'),
                'parent': representation.pop('parent'),
            }
        }


class FinancialTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialTransaction
        fields = '__all__'
        read_only_fields = ['timestamp', 'linked']

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        transaction = instance
        category = transaction.category
        operator = transaction.operator
        account = transaction.account
        contact = transaction.contact
        return {
            'transaction': {
                'id': representation.pop('id'),
                'description': representation.pop('description'),
                'amount': representation.pop('amount'),
                'type': representation.pop('type'),
                'timestamp': representation.pop('timestamp'),
                'category': {
                    'id': category.id if category else None,
                    'name': category.name if category else None,
                },
                'operator': {
                    'id': operator.id if operator else None,
                    'name': operator.name if operator else None,            
                },
                'account': {
                    'id': account.id if account else None,
                    'name': account.name if account else None,
                },
                'contact': {
                    'name': str(contact) if contact else None,
                    'id': contact.id if contact else None,
                },
                'payment': representation.pop('payment'),
                'linked': representation.pop('linked'),
            }
        }


    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        business = self.context['business']
        data = self.context['data']

        transaction = super().create(validated_data)

        is_transfer = transaction.type == 'transfer'
        if is_transfer:
            transfer = complete_transfer(business, data, request, transaction)
        
            if transfer:
                operator_description = data.get('description', None)
                transfer_description = f'Transfer Sent to {transfer.account}'
                description = f'{transfer_description} • {operator_description}'
                transaction.description = description
                transaction.save()
        
        return transaction
