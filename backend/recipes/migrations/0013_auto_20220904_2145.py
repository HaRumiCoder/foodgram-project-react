# Generated by Django 2.2.16 on 2022-09-04 18:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_remove_recipe_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.Recipe', verbose_name='Рецепт'),
        ),
    ]
