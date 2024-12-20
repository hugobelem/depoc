from rest_framework import serializers

from .models import Business, BusinessOwner # type: ignore


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            'id',
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
            'city',
            'state',
            'postCode',
            'phone',
            'email',            
        ]
        required = ['legalName', 'tradeName', 'registrationNumber']
        
    
    def create(self, validated_data):
        business = Business.objects.create(**validated_data)
        return business
    
    
    def update(self, instance, validated_data):
        Business.objects.filter(id=instance.id).update(**validated_data)
        instance.refresh_from_db()
        return instance
