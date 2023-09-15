# Generated by Django 4.1.4 on 2023-05-31 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomtech', '0009_alter_transaction_trx_totalamt'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_by', models.CharField(max_length=50, null=True)),
                ('review_email', models.EmailField(max_length=50, null=True)),
                ('review_content', models.TextField(null=True)),
                ('review_ratings', models.IntegerField(null=True)),
                ('review_date', models.DateField(auto_now=True)),
                ('review_for', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prod_rev', to='ecomtech.product')),
            ],
        ),
    ]
