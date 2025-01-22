from django.db import models


class Inventory(models.Model):
    id = models.CharField(
        max_length=26,
        primary_key=True,
        unique=True,
        editable=False,
    )  

    product = models.OneToOneField(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='inventory',
    )

    quantity = models.IntegerField(default=0)
    reserved = models.IntegerField(default=0)
    location = models.CharField(max_length=150, blank=True, null=True)


    def __str__(self):
        return f'Inventory for {self.product}'


class InventoryTransaction(models.Model):
    TRANSACTION_TYPE = [
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
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

    type = models.CharField(max_length=100, choices=TRANSACTION_TYPE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.type
