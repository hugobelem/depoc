from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction

from rest_framework import serializers

from .models import User, Owner


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = [
            'is_superuser',
            'is_staff',
            'is_active',
            'last_login',
            'date_joined',
            'groups',
            'user_permissions',
        ]


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'user': {
                'id': representation.pop('id'),
                'name': representation.pop('name'),
                'email': representation.pop('email'),
                'username': representation.pop('username'),
                'is_active': representation.pop('is_active'),
                'is_staff': representation.pop('is_staff'),
                'last_login': representation.pop('last_login'),
                'date_joined': representation.pop('date_joined'),
            }
        }


    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        
        return value


    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(is_staff=True, **validated_data)
        user.set_password(user.password)
        user.save()
        Owner.objects.create(user=user)

        return user


    def update(self, instance, validated_data):
        validated_data.pop('password', None)

        return super().update(instance, validated_data)


class OwnerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Owner
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'owner': {
                'id': representation.pop('id'),
                'name': representation.pop('name'),
                'email': representation.pop('email'),
                'phone': representation.pop('phone'),
            }
        }
