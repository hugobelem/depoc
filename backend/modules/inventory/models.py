from django.db import models


class Inventory(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )  
    product = models.OneToOneField(
        'modules_products.Products',
        on_delete=models.CASCADE,
        related_name='inventory',
    )
    quantity = models.IntegerField(default=0)
    reserved = models.IntegerField(default=0)
    location = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name_plural = 'Inventory'
        app_label = 'modules_inventory'

    def __str__(self):
        return f'Inventory for {self.product}'


class InventoryTransaction(models.Model):
    TRANSACTION_TYPE = [
        ('entrada', 'Entrada'),
        ('saída', 'Saída'),
        ('balanço', 'Balanço'),
    ]
    
    id = models.CharField(
        max_length=25,
        primary_key=True,
        unique=True,
        editable=False,
    )
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    transactionType = models.CharField(max_length=100, choices=TRANSACTION_TYPE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    unitCost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Inventory Transactions'
        app_label = 'modules_inventory'

    def __str__(self):
        return self.transactionType
