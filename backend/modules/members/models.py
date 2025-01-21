from django.db import models


class Member(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )

    business = models.ForeignKey(
        'business.Business',
        on_delete=models.CASCADE,
        related_name='members',
    )

    credential = models.OneToOneField(
        'accounts.User',
         on_delete=models.CASCADE,
         related_name='member',
         blank=True,
         null=True,
    )

    name = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)  
    role = models.CharField(max_length=150, blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)

    salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
    )

    phone = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    has_access = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
