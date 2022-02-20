# Generated by Django 4.0.2 on 2022-02-18 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_orderitem_size_remove_product_available_sizes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColourVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='orderitem',
            name='colour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.colourvariation'),
        ),
        migrations.AddField(
            model_name='product',
            name='available_colours',
            field=models.ManyToManyField(to='cart.ColourVariation'),
        ),
    ]
