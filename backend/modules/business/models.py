# type: ignore

from django.db import models
from django.contrib.auth import get_user_model

import ulid

User = get_user_model()


class Business(models.Model):
    id = models.CharField(
        primary_key=True, max_length=26, default=ulid.new().str
    )
    owner = models.OneToOneField(
        User, related_name='businesses', on_delete=models.CASCADE
    )
    legalName = models.CharField(max_length=150)
    tradeName = models.CharField(max_length=150)
    registrationNumber = models.CharField(max_length=14, unique=True)
    stateRegistration = models.CharField(max_length=14, blank=True)
    cityRegistration = models.CharField(max_length=14, blank=True)
    companyType = models.CharField(max_length=150, blank=True)
    streetAddress = models.CharField(max_length=150, blank=True)
    addressNumber = models.CharField(max_length=10, blank=True)
    neighborhood = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=2, blank=True)
    postCode = models.CharField(max_length=8, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    email = models.EmailField(blank=True)    
    category = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return self.cnpj
