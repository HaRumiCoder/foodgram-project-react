from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCartRecipe, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    list_filter = ("author", "name", "tags")


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    list_filter = ("user", "recipe")


class ShoppingCartRecipeAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    list_filter = ("user", "recipe")


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "recipe")
    list_filter = ("recipe",)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(ShoppingCartRecipe, ShoppingCartRecipeAdmin)
