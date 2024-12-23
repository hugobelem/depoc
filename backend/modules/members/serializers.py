from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.apps import apps

from modules.members.models import Members, MembersCredentials

import ulid

User = get_user_model()
Business = apps.get_model('modules_business', 'Business')
BusinessOwner = apps.get_model('modules_business', 'BusinessOwner')
BusinessMembers = apps.get_model('modules_business', 'BusinessMembers')


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = [
            'firstName',
            'lastName',
            'taxId',
            'dateOfBirth',
            'role',
            'status',
            'hireDate',
            'position',
            'salary',
            'streetAddress',
            'addressNumber',
            'neighborhood',
            'city',
            'state',
            'postCode',
            'phone',
            'email',
            'access',   
        ]
        required = ['firstName', 'lastName', 'taxId', 'salary', 'email']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'id': instance.id,
            'details': {
                'firstName': representation.pop('firstName'),
                'lastName': representation.pop('lastName'),
                'taxId': representation.pop('taxId'),
                'dateOfBirth': representation.pop('dateOfBirth'),
                'role': representation.pop('role'),
                'status': representation.pop('status'),
                'hireDate': representation.pop('hireDate'),
                'position': representation.pop('position'),
                'salary': representation.pop('salary'),
                'address': {
                    'streetAddress': representation.pop('streetAddress'),
                    'addressNumber': representation.pop('addressNumber'),
                    'neighborhood': representation.pop('neighborhood'),
                    'city': representation.pop('city'),
                    'state': representation.pop('state'),
                    'postCode': representation.pop('postCode'),
                },
                'contact': {
                    'phone': representation.pop('phone'),
                    'email': representation.pop('email'),                    
                },
                'access': representation.pop('access'),
            },
        }        
        
    
    def create(self, validated_data):
        try:
            owner = self.context['owner']
            get_owner = BusinessOwner.objects.get(owner=owner)
            business = get_owner.business
        except BusinessOwner.DoesNotExist:
            message = 'Failed to associate member.'
            raise serializers.ValidationError({'error': message})      

        member = Members.objects.create(id=ulid.new().str, **validated_data)
        BusinessMembers.objects.create(
            id=ulid.new().str,
            member=member,
            business=business
        ) 

        if member.access:
            name = str(validated_data['firstName']) + str(validated_data['lastName'])
            email= validated_data['email']
            credentials = User.objects.create(
                id=ulid.new().str,
                name=name,
                email=email,
                is_staff=True
            )
            MembersCredentials.objects.create(
                id=ulid.new().str,
                member=member,
                credentials=credentials
            )

        return member


    def update(self, instance, validated_data):
        member = self.context['member']
        Members.objects.filter(id=member.id).update(**validated_data)
        instance.refresh_from_db()
        return instance