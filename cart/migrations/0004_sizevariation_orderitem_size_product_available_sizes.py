# Generated by Django 4.0.2 on 2022-02-18 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_address_order_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='SizeVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cart.sizevariation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='available_sizes',
            field=models.ManyToManyField(to='cart.SizeVariation'),
        ),
    ]
