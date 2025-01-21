from rest_framework import serializers

from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Member

User = get_user_model()


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        member = instance
        return {
            'member': {
                'id': representation.pop('id'),
                'name': representation.pop('name'),
                'cpf': representation.pop('cpf'),
                'date_of_birth': representation.pop('date_of_birth'),
                'role': representation.pop('role'),
                'hire_date': representation.pop('hire_date'),
                'salary': representation.pop('salary'),
                'phone': representation.pop('phone'),
                'email': representation.pop('email'),
                'has_access': representation.pop('has_access'),
                'is_active': representation.pop('is_active'),
                'credential': {
                    'id': representation.pop('credential'),
                    'username': member.credential.username,
                },
            }
        }


    @transaction.atomic
    def create(self, validated_data):
        member = super().create(validated_data)

        if member.has_access:
            credential = User.objects.create_user(
                name=member.name,
                email=member.email,
                username=member.phone,
                password=member.id,
                is_staff=True,
            )

            member.credential = credential
            member.save()

        return member
