from django.contrib import admin

from .models import Favorite, Ingredient, IngredientRecipe, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    list_filter = ("author", "name", "tags")


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(IngredientRecipe)
