# Generated by Django 4.0.3 on 2022-05-27 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderid',
            name='amount',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderid',
            name='quantity',
            field=models.CharField(default=0, max_length=8),
            preserve_default=False,
        ),
    ]
