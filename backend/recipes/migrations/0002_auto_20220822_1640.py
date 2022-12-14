# Generated by Django 2.2.16 on 2022-08-22 13:40

from django.db import migrations, models

import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=models.CharField(
                max_length=7,
                unique=True,
                validators=[recipes.validators.validate_hex_code],
                verbose_name="Цвет",
            ),
        ),
    ]
