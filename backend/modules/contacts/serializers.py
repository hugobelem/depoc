from rest_framework import serializers

from .models import Contacts


class ContactsSerializer(serializers):
    class Meta:
        model = Contacts
        fields = [
            'name',
            'alias',
            'code',
            'entityType',
            'entityId',
            'taxPayer',
            'companyTaxCategory',
            'stateRegistration',
            'cityRegistration',
            'contactType',
            'postCode',
            'city',
            'state',
            'streetAddress',
            'addressNumber',
            'neighborhood',
            'additionalInfo',
            'phone',
            'email',
            'dateOfBirth',
            'gender',
            'maritalStatus',
            'notes',
            'status',
        ]
        required = ['name', 'code', 'entityType', 'entityId', 'contactType']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'id': instance.id,
            'details': {
                'name': representation.pop('name'),
                'alias': representation.pop('alias'),
                'code': representation.pop('code'),
                'entityType': representation.pop('entityType'),
                'entityId': representation.pop('entityId'),
                'contactType': representation.pop('contactType'),               
                'companyInfo': {
                    'taxPayer': representation.pop('taxPayer'),
                    'companyTaxCategory': representation.pop('companyTaxCategory'),
                    'stateRegistration': representation.pop('stateRegistration'),
                    'cityRegistration': representation.pop('cityRegistration'),
                },
                'address': {
                    'streetAddress': representation.pop('streetAddress'),
                    'addressNumber': representation.pop('addressNumber'),
                    'neighborhood': representation.pop('neighborhood'),
                    'additionalInfo': representation.pop('additionalInfo'),
                    'city': representation.pop('city'),
                    'state': representation.pop('state'),
                    'postCode': representation.pop('postCode'),
                },
                'contact': {
                    'phone': representation.pop('phone'),
                    'email': representation.pop('email'),                    
                },
                'outro': {
                    'dateOfBirth': representation.pop('dateOfBirth'),
                    'gender': representation.pop('gender'),
                    'maritalStatus': representation.pop('maritalStatus'),
                    'notes': representation.pop('notes'),
                    'status': representation.pop('status'),
                    'created': instance.created,                 
                }
            },
        }
