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
            'additionalInfo',
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
                    'additionalInfo': representation.pop('additionalInfo'),
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
        business = self.context['business']  
        member_id = ulid.new().str
        member = Members.objects.create(id=member_id, **validated_data)

        business_members_id = ulid.new().str
        BusinessMembers.objects.create(
            id=business_members_id,
            member=member,
            business=business
        )

        if member.access:
            name = f"{validated_data['firstName']} {validated_data['lastName']}"
            email= validated_data['email']

            credential_id = ulid.new().str
            credential = User.objects.create(
                id=credential_id,
                name=name,
                email=email,
                is_staff=True
            )
            
            credential_id = ulid.new().str
            MembersCredentials.objects.create(
                id=credential_id,
                member=member,
                credential=credential
            )

        return member


    def update(self, instance, validated_data):
        members = self.context['members']
        Members.objects.filter(id=members.member.id).update(**validated_data)
        instance.refresh_from_db()
        return instance
