from django.db import models


class Contacts(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )
    name = models.CharField(max_length=150, blank=False)
    alias = models.CharField(max_length=150, blank=True)
    code = models.CharField(max_length=50, blank=False, unique=True)
    entityType = models.CharField(max_length=10, blank=False)
    taxId = models.CharField(max_length=14, blank=False, unique=True)
    taxPayer = models.CharField(max_length=150, blank=False, unique=True)
    companyTaxCategory = models.CharField(max_length=50, blank=True)
    stateRegistration = models.CharField(max_length=14, blank=True)
    cityRegistration = models.CharField(max_length=14, blank=True)
    contactType = models.CharField(max_length=10, blank=False)
    postCode = models.CharField(max_length=8, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=2, blank=True)
    streetAddress = models.CharField(max_length=150, blank=True)
    addressNumber = models.CharField(max_length=10, blank=True)
    neighborhood = models.CharField(max_length=50, blank=True)
    additionalInfo = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    dateOfBirth = models.DateField(blank=True, null=True) 
    gender = models.CharField(max_length=50, blank=True)
    maritalStatus = models.CharField(max_length=50, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=150, blank=True)


    class Meta:
        verbose_name_plural = 'Contacts'
        app_label = 'modules_contacts'

    def __str__(self):
        return f'{self.name} - {self.taxId}'   
