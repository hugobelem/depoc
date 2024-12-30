from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Products(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )
    name = models.CharField(max_length=150, blank=False)
    sku = models.CharField(max_length=100, blank=True, unique=True)
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True
    )
    unit = models.CharField(max_length=50, blank=True)
    stock = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    trackStock = models.BooleanField(default=True)
    brand = models.CharField(max_length=100, blank=True)
    origin = models.CharField(max_length=100, blank=True)
    ncm = models.CharField(max_length=10, blank=True)
    barcode = models.IntegerField(blank=True, null=True)
    cest = models.CharField(max_length=20, blank=True)
    category = models.ForeignKey(
        'modules_products.Category', 
        on_delete=models.PROTECT, 
        related_name='products',
        blank=True,
        null=True,
    )
    costPrice = models.DecimalField(
	    max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
	   )
    retailPrice = models.DecimalField(
	    max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
	   )
    discountedPrice = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Products'
        app_label = 'modules_products'
    
    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )
    name = models.CharField(max_length=150, unique=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='subcategories',
    )

    class Meta:
        verbose_name_plural = 'Categories'
        app_label = 'modules_products'
    
    def __str__(self):
        return self.name


class CostHistory(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )
    product = models.ForeignKey(
        Products,
        related_name='cost_history',
        on_delete=models.CASCADE,
    )
    source = models.CharField(max_length=100, blank=True)
    quatity = models.PositiveIntegerField(default=0)
    effectiveDate = models.DateField()
    costPrice = models.DecimalField(max_digits=10, decimal_places=2)
    costAverage = models.DecimalField(max_digits=10, decimal_places=2)
    retailPrice = models.DecimalField(max_digits=10, decimal_places=2)
    markup = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Cost History'
        app_label = 'modules_products'

    def __str__(self):
        return f"Cost History for {self.product} on {self.effectiveDate}"


class ProductSource(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )
    product = models.OneToOneField(
        Products,
        related_name='source',
        on_delete=models.CASCADE,
    )
    source_content_type = models.ForeignKey(
        ContentType,
        related_name='product_sources',
        on_delete=models.CASCADE,
    )
    source_object_id = models.CharField(max_length=50)
    source = GenericForeignKey('source_content_type', 'source_object_id')

    class Meta:
        verbose_name_plural = 'Sources'
        app_label = 'modules_products'

    def __str__(self):
        return f"{self.product.name} - {self.source}"
