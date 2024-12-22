from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Members(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )
    firstName = models.CharField(max_length=150)
    lastName = models.CharField(max_length=150)
    personalId = models.CharField(max_length=11, blank=True)
    dateOfBirth = models.DateField(blank=True, null=True)    
    role = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=150, blank=True)
    hireDate = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=150, blank=True)    
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    streetAddress = models.CharField(max_length=150, blank=True)
    addressNumber = models.CharField(max_length=10, blank=True)
    neighborhood = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=2, blank=True)
    postCode = models.CharField(max_length=8, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    email = models.EmailField()
    access = models.BooleanField(default=False)    

    class Meta:
        verbose_name_plural = 'Members'
        app_label = 'modules_members'

    def __str__(self):
        return f'{self.firstName} {self.lastName}'    


class MembersCredentials(models.Model):
    member = models.OneToOneField(Members, on_delete=models.CASCADE)
    credentials = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Credentials'
        app_label = 'modules_members'
