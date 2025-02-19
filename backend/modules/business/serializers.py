from rest_framework import serializers

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
                'cnpj': representation.pop('cnpj'),
                'ie': representation.pop('ie'),
                'im': representation.pop('im'),
                'is_active': representation.pop('is_active'),
                'postcode': representation.pop('postcode'),
                'city': representation.pop('city'),
                'state': representation.pop('state'),
                'address': representation.pop('address'),
                'phone': representation.pop('phone'),
                'email': representation.pop('email'),                    
            }
        }        
        
    
    def create(self, validated_data):
        business = super().create(validated_data)

        owner = self.context['owner']
        owner.business = business
        owner.save()

        return business
