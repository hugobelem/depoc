from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from modules.members.models import Members, MembersCredentials

import ulid

User = get_user_model()


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Members
        fields = [
            'firstName',
            'lastName',
            'personalId',
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
        required = ['firstName', 'lastName', 'salary']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'id': instance.id,
            'details': {
                'firstName': representation.pop('firstName'),
                'lastName': representation.pop('lastName'),
                'personalId': representation.pop('personalId'),
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
        member = Members.objects.create(id=ulid.new().str, **validated_data)
        if member.access:
            name = str(validated_data['firstName']) + str(validated_data['lastName'])
            email= validated_data['email']

            credentials = User.objects.create(
                id=ulid.new().str,
                name=name,
                email=email,
                is_staff=True
            )

            MembersCredentials.objects.create(member=member, credentials=credentials)
        return member
