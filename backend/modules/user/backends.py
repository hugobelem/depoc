from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models

class EmailOrUsernameBackend(ModelBackend):
    '''
    Allow users to authenticate using both email or username.
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(
                models.Q(email=username) | models.Q(username=username)
                )
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None