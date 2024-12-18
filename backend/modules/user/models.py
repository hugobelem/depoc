# type: ignore
import ulid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.CharField(
        primary_key=True, max_length=26, default=ulid.new().str
    )
    first_name = None
    last_name = None
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=False, null=False)
    username = models.CharField(
        max_length=150, unique=True, blank=True, null=True,
    )

    REQUIRED_FIELDS = ['email']

    def __str__(self) -> str:
        return self.email
