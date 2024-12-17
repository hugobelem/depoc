from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
