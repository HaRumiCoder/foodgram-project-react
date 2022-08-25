from django.contrib.auth import get_user_model
from django.db import models

from .validators import validate_hex_code

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="Название")
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name="Цвет",
        validators=[validate_hex_code]
    )
    slug = models.SlugField(
        max_length=30,
        unique=True
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Ingredient(models.Model):
    name = models.CharField(
        max_length=30,
        verbose_name="Имя"
    )
    measurement_unit = models.CharField(
        max_length=30,
        verbose_name="Единица измерения"
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class Recipe(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Цвет"
    )
    text = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание"
    )
    image = models.ImageField(
        upload_to="recipes/",
        verbose_name="Картинка"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="recipes"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="Теги"
    )
    cooking_time = models.PositiveIntegerField(verbose_name="Время")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Ингредиент",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="Рецепт",
    )
    amount = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Ингредиент-Рецепт"
        verbose_name_plural = "Ингредиент-Рецепт"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="favorite_for",
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite")
        ]


class ShoppingCartRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shopping_cart_recipes",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="in_shopping_carts",
    )

    class Meta:
        verbose_name = "Рецепт из списка покупок"
        verbose_name_plural = "Рецепты из списка покупок"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_shopping_cart_item"
            )
        ]