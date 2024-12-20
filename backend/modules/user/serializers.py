from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'name', 
            'email', 
            'username', 
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True},}
        post_required = ['name', 'email', 'username', 'password']
        patch_required = ['name', 'email', 'username']


    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value        


    def create(self, validated_data):
        user = User.objects.create_superuser(**validated_data)
        return user
    
    
    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        
        User.objects.filter(id=instance.id).update(**validated_data)
        instance.refresh_from_db()
        return instance

