from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None

    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )

    name = models.CharField(max_length=255)

    email = models.EmailField(
        unique=True,
        blank=False,
        null=False
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = ['email']

    def __str__(self) -> str:
        return self.email


class Owner(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='owner',
    )

    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=14,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.name
