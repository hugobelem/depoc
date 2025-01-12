from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.apps import apps

from modules.members.models import Members, MembersCredentials

User = get_user_model()
Business = apps.get_model('modules_business', 'Business')
BusinessOwner = apps.get_model('modules_business', 'BusinessOwner')
BusinessMembers = apps.get_model('modules_business', 'BusinessMembers')


def assign_member_to_business(member, business):
    BusinessMembers.objects.create(
        member=member,
        business=business
    )


def create_member_credential(member, validated_data):
    if member.access:
        name = f"{validated_data['firstName']} {validated_data['lastName']}"
        email= validated_data['email']

        credential = User.objects.create(
            name=name,
            email=email,
            is_staff=True
        )

        MembersCredentials.objects.create(
            member=member,
            credential=credential
        )


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
        member = Members.objects.create(**validated_data)

        assign_member_to_business(member=member, business=business)
        create_member_credential(member=member, validated_data=validated_data)

        return member


    def update(self, instance, validated_data):
        Members.objects.filter(id=instance.id).update(**validated_data)
        instance.refresh_from_db()
        return instance
