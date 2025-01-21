from django.db import models


class Contact(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )
    
    is_active = models.BooleanField(default=True)
    
    code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
    )

    phone = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    postcode = models.CharField(max_length=8, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


    def __str__(self):
        if hasattr(self, 'customer'):
            return self.customer.name
        elif hasattr(self, 'supplier'):
            return self.supplier.legal_name
        return 'Contact'


class Customer(Contact):
    GENDER_TYPES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unkown', 'Unkown'),
    ]

    name = models.CharField(max_length=150, db_index=True)
    alias = models.CharField(max_length=150, blank=True, null=True, db_index=True)

    cpf = models.CharField(
        max_length=11,
        unique=True,
        blank=True,
        null=True, 
        db_index=True,
    )

    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    number_of_orders = models.PositiveIntegerField(default=0)

    gender = models.CharField(
        choices=GENDER_TYPES,
        max_length=50,
        blank=True,
        null=True,
    )

    business = models.ForeignKey(
        'business.Business',
        on_delete=models.CASCADE,
        related_name='customers',
        blank=True,
        null=True
    )


    def __str__(self):
        return self.name 


class Supplier(Contact):
    legal_name = models.CharField(max_length=150, db_index=True)

    trade_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        db_index=True
    )

    cnpj = models.CharField(
        max_length=14,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
    
    )
    
    ie = models.CharField(max_length=14, blank=True, null=True)
    im = models.CharField(max_length=14, blank=True, null=True)

    business = models.ForeignKey(
        'business.Business',
        on_delete=models.CASCADE,
        related_name='suppliers',
        blank=True,
        null=True
    )


    def __str__(self):
        return self.legal_name 
