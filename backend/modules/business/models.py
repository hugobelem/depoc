from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Business(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
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
    additionalInfo = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state = models.CharField(max_length=2, blank=True)
    postCode = models.CharField(max_length=8, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    email = models.EmailField(blank=True, null=True)    
    category = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Businesses'
        app_label = 'modules_business'

    def __str__(self):
        return self.legalName


class BusinessOwner(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )    
    owner = models.OneToOneField(
        User,
        related_name='business',
        on_delete=models.CASCADE
    )
    business = models.OneToOneField(
        Business,
        related_name='owner',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Business Owners'
        app_label = 'modules_business'   

    def __str__(self):
        return f'{self.owner} owns {self.business}'
    

class BusinessMembers(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )    
    member = models.ForeignKey(
        'modules_members.Members',
        related_name='business',
        on_delete=models.CASCADE
    )
    business = models.ForeignKey(
        Business,
        related_name='members',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Business Members'
        app_label = 'modules_business'   

    def __str__(self):
        return f'{self.member} - {self.business}'


class BusinessContacts(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )    
    contact = models.ForeignKey(
        'modules_contacts.Contacts',
        related_name='business_contacts',
        on_delete=models.CASCADE
    )
    business = models.ForeignKey(
        Business,
        related_name='business_contacts',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Business Contacts'
        app_label = 'modules_business'

    def __str__(self):
        return f'{self.contact} - {self.business}'


class BusinessProducts(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )    
    product = models.ForeignKey(
        'modules_products.Products',
        related_name='business_products',
        on_delete=models.CASCADE
    )
    business = models.ForeignKey(
        Business,
        related_name='business_products',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Business Products'
        app_label = 'modules_business'

    def __str__(self):
        return f'{self.product} - {self.business}'


class BusinessProductsCategories(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )
    category = models.ForeignKey(
        'modules_products.Category',
        related_name='product_categories',
        on_delete=models.CASCADE
    )
    business = models.ForeignKey(
        Business,
        related_name='categories',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Business Products Categories'
        app_label = 'modules_business'

    def __str__(self):
        return f'{self.category} - {self.business}'


class BusinessBankAccounts(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )
    bankAccount = models.ForeignKey(
        'modules_finance.BankAccount',
        on_delete=models.CASCADE,
        related_name='business',
    )
    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name='bank_accounts'
    )

    class Meta:
        verbose_name_plural = 'Business Bank Accounts'

    def __str__(self):
        return f'{self.bankAccount} - {self.business}'
