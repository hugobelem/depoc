from rest_framework import serializers

from modules.members.models import Members, MembersCredentials

import ulid


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
        credentials = self.context['credentials']
        member = Members.objects.create(id=ulid.new().str, **validated_data)

        if member.access:
            MembersCredentials.objects.create(
                member=member,
                credentials=credentials
            )
        return member
