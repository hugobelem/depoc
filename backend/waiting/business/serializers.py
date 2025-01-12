from rest_framework import serializers

from modules.business.models import Business, BusinessOwner


def assign_business_to_owner(owner, business) -> None:
    BusinessOwner.objects.create(
        owner=owner,
        business=business
    )


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            'legalName',
            'tradeName',
            'registrationNumber',
            'stateRegistration',
            'cityRegistration',
            'companyType',
            'category',
            'streetAddress',
            'addressNumber',
            'neighborhood',
            'additionalInfo',
            'city',
            'state',
            'postCode',
            'phone',
            'email',            
        ]
        required = ['legalName', 'tradeName', 'registrationNumber']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'id': instance.id,
            'details': {
                'legalName': representation.pop('legalName'),
                'tradeName': representation.pop('tradeName'),   
                'registrationNumber': representation.pop('registrationNumber'),
                'stateRegistration': representation.pop('stateRegistration'),
                'cityRegistration': representation.pop('cityRegistration'),
                'companyType': representation.pop('companyType'),
                'category': representation.pop('category'),
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
                }
            },
        }        
        
    
    def create(self, validated_data):
        owner = self.context['owner']
        business = Business.objects.create(**validated_data)
        assign_business_to_owner(owner=owner, business=business)
        return business
    
    
    def update(self, instance, validated_data):
        Business.objects.filter(id=instance.id).update(**validated_data)
        instance.refresh_from_db()
        return instance
