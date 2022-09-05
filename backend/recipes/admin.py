from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCartRecipe, Tag)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ("name", "author__id", "tags__id")
    list_display = ("name", "author", "favorite_count")
    list_filter = ("author", "name", "tags")
    inlines = [IngredientRecipeInline]

    def favorite_count(self, obj):
        return obj.favorite_for.count()


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)
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
