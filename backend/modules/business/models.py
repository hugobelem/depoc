from django.db import models


class Business(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )
    legal_name = models.CharField(max_length=150)
    trade_name = models.CharField(max_length=150)
    registration_number = models.CharField(max_length=14, unique=True)
    state_registration = models.CharField(max_length=14, blank=True)
    city_registration = models.CharField(max_length=14, blank=True)
    street_address = models.CharField(max_length=150, blank=True)
    address_number = models.CharField(max_length=10, blank=True)
    neighborhood = models.CharField(max_length=50, blank=True)
    additional_info = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=2, blank=True)
    postcode = models.CharField(max_length=8, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.legal_name
