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
        required = ['name', 'email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_superuser(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        
        User.objects.filter(id=instance.id).update(**validated_data)
        instance.refresh_from_db()
        return instance

