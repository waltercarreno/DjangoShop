# Generated by Django 4.0.2 on 2022-02-18 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_sizevariation_orderitem_size_product_available_sizes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='size',
        ),
        migrations.RemoveField(
            model_name='product',
            name='available_sizes',
        ),
        migrations.DeleteModel(
            name='SizeVariation',
        ),
    ]
