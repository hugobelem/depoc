from django.db import models


class Product(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )

    name = models.CharField(max_length=150, db_index=True)
    
    sku = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
    )

    barcode = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    brand = models.CharField(max_length=100, blank=True, null=True)

    business = models.ForeignKey(
        'business.Business',
        on_delete=models.CASCADE,
        related_name='products',
    )

    category = models.ForeignKey(
        'products.ProductCategory', 
        on_delete=models.PROTECT, 
        related_name='products',
        blank=True,
        null=True,
    )

    supplier= models.ManyToManyField(
        'contacts.Supplier',
        related_name='products',
        blank=True,
        null=True,
    )

    cost_price = models.DecimalField(
	    max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
	)
    
    retail_price = models.DecimalField(
	    max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
	)
    
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    unit = models.CharField(max_length=50, blank=True, null=True)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    track_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )

    business = models.ForeignKey(
        'business.Business',
        on_delete=models.CASCADE,
        related_name='product_categories',
    )
    
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name='subcategories',
        blank=True, 
        null=True, 
    )

    name = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name


class ProductCostHistory(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False
    )

    product = models.ForeignKey(
        Product,
        related_name='cost_history',
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField()
    effective_date = models.DateField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)

    average_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    markup = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Cost History for {self.product} on {self.effective_date}"
