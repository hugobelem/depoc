from rest_framework import serializers

from django.db import transaction

from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'business': {
                'id': instance.id,
                'legal_name': representation.pop('legal_name'),
                'trade_name': representation.pop('trade_name'),   
                'registration_number': representation.pop('registration_number'),
                'state_registration': representation.pop('state_registration'),
                'city_registration': representation.pop('city_registration'),
                'address': {
                    'street_address': representation.pop('street_address'),
                    'address_number': representation.pop('address_number'),
                    'neighborhood': representation.pop('neighborhood'),
                    'additional_info': representation.pop('additional_info'),
                    'city': representation.pop('city'),
                    'state': representation.pop('state'),
                    'postcode': representation.pop('postcode'),
                },
                'contact': {
                    'phone': representation.pop('phone'),
                    'email': representation.pop('email'),                    
                },
                'is_active': representation.pop('is_active'),
            }
        }        
        
    
    @transaction.atomic()
    def create(self, validated_data):
        business = super().create(validated_data)

        owner = self.context['owner']
        owner.business = business
        owner.save()

        return business
