from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models


class EmailOrUsernameAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(
                models.Q(email=username) | models.Q(username=username)
                )
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
