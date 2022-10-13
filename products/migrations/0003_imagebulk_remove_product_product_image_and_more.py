# Generated by Django 4.1 on 2022-08-12 09:32

import django.core.validators
from django.db import migrations, models
import ecom.validators


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_product_views"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImageBulk",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="media/product",
                        validators=[
                            ecom.validators.check_image,
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["png", "jpg", "svg", "jpeg"]
                            ),
                        ],
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="product",
            name="product_image",
        ),
        migrations.AddField(
            model_name="product",
            name="product_image",
            field=models.ManyToManyField(to="products.imagebulk"),
        ),
    ]
