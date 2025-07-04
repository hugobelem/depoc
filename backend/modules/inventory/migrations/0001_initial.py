# Generated by Django 5.1.4 on 2025-02-13 22:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.CharField(editable=False, max_length=26, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.IntegerField(default=0)),
                ('reserved', models.IntegerField(default=0)),
                ('location', models.CharField(blank=True, max_length=150, null=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryTransaction',
            fields=[
                ('id', models.CharField(editable=False, max_length=25, primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(choices=[('inbound', 'Inbound'), ('outbound', 'Outbound')], max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
                ('unit_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='inventory.inventory')),
            ],
        ),
    ]
