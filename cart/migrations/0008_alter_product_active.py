# Generated by Django 4.0.2 on 2022-02-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_product_active_alter_order_billing_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]