# Generated by Django 4.1.4 on 2022-12-20 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomtech', '0003_customer_cust_password_alter_customer_cust_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity_added',
            field=models.IntegerField(default='1', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='prod_image',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
