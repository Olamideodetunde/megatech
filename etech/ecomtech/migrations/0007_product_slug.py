# Generated by Django 4.1.4 on 2022-12-31 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomtech', '0006_product_product_description_alter_product_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
