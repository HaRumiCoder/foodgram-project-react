# Generated by Django 2.2.16 on 2022-08-22 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0002_auto_20220822_1640"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="cooking_time",
            field=models.PositiveIntegerField(default=1, verbose_name="Время"),
            preserve_default=False,
        ),
    ]
