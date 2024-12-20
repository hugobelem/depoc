from rest_framework import serializers

from modules.business.models import Business, BusinessOwner

import ulid


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
        expected = [field for field in fields if field != 'id']
        
    
    def create(self, validated_data):
        owner = self.context['owner']
        business = Business.objects.create(
            id=ulid.new().str,
            **validated_data
        )
        
        BusinessOwner.objects.create(owner=owner, business=business)
        return business
    
    
    def update(self, instance, validated_data):
        Business.objects.filter(id=instance.id).update(**validated_data)
        instance.refresh_from_db()
        return instance
