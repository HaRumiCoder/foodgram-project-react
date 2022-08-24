import base64
import uuid

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from djoser import serializers as djoser_serializers
from recipes.models import Favorite, Ingredient, IngredientRecipe, Recipe, Tag, ShoppingCartRecipe
from rest_framework import serializers
from users.models import Subscription

User = get_user_model()

RE_FAVORITE_ERROR = "Нельзя подписываться на рецепт повторно!"

RE_SUBSCRIBTION_ERROR = "Нельзя подписываться на пользователя повторно!"

SUBSCRIBE_TO_YOURSELF_ERROR = "Нельзя подписываться на себя!"


class IsSubscribed:
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            subscribed_to=obj if obj is User else obj.subscribed_to,
            subscriber=self.context.get("request").user,
        ).exists()


class CreateUserSerializer(djoser_serializers.UserCreateSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name", "password")


class UserSerialiser(serializers.ModelSerializer, IsSubscribed):
    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name")


class ImageBase64(serializers.Field):
    def to_representation(self, value):
        return value.url

    def to_internal_value(self, data):
        filename = str(uuid.uuid4()) + ".png"
        return ContentFile(base64.b64decode(data.split(",")[1]), filename)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredient.id")

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")

    def create(self, validated_data):
        IngredientRecipe.objects.create(
            ingredient=Ingredient.get(pk=validated_data["id"]),
            amount=validated_data["amount"],
        )


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True)
    author = UserSerialiser(read_only=True)
    image = ImageBase64()

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
            "author",
        )

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")

        recipe = Recipe.objects.create(**validated_data)

        recipe.tags.set(tags)

        for ingredient in ingredients:
            ingredient_data = IngredientRecipeSerializer(ingredient).data
            IngredientRecipe.objects.create(
                ingredient=get_object_or_404(Ingredient, pk=ingredient_data["id"]),
                amount=ingredient_data["amount"],
                recipe=recipe,
            )

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.tags.set(tags)
        instance.ingredients.all().delete()
        for ingredient in ingredients:
            ingredient_data = IngredientRecipeSerializer(ingredient).data
            IngredientRecipe.objects.create(
                ingredient=get_object_or_404(Ingredient, pk=ingredient_data["id"]),
                amount=ingredient_data["amount"],
                recipe=instance,
            )
        instance.save()
        return instance


class SubscribeSerializer(serializers.ModelSerializer, IsSubscribed):
    email = serializers.ReadOnlyField(source="subscribed_to.email")
    id = serializers.ReadOnlyField(source="subscribed_to.id")
    username = serializers.ReadOnlyField(source="subscribed_to.username")
    first_name = serializers.ReadOnlyField(source="subscribed_to.first_name")
    last_name = serializers.ReadOnlyField(source="subscribed_to.last_name")

    class Meta:
        model = Subscription
        fields = ("email", "id", "username", "first_name", "last_name")

    def validate(self, data):
        subscribed_to_id = self.context["view"].kwargs.get("user_id")
        subscribed_to = get_object_or_404(User, pk=subscribed_to_id)
        if Subscription.objects.filter(
            subscriber=self.context["request"].user, subscribed_to=subscribed_to
        ).exists():
            raise serializers.ValidationError({"errors": RE_SUBSCRIBTION_ERROR})
        if subscribed_to == self.context["request"].user:
            raise serializers.ValidationError({"errors": SUBSCRIBE_TO_YOURSELF_ERROR})
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="recipe.name")
    id = serializers.ReadOnlyField(source="recipe.id")
    image = ImageBase64(source="recipe.image")
    cooking_time = serializers.ReadOnlyField(source="recipe.cooking_time")

    class Meta:
        model = Favorite
        fields = ("id", "name", "image", "cooking_time")

    def validate(self, data):
        recipe_id = self.context["view"].kwargs.get("recipe_id")
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if Favorite.objects.filter(
            user=self.context["request"].user, recipe=recipe
        ).exists():
            raise serializers.ValidationError({"errors": _(RE_SUBSCRIBTION_ERROR)})
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="recipe.name")
    id = serializers.ReadOnlyField(source="recipe.id")
    image = ImageBase64(source="recipe.image")
    cooking_time = serializers.ReadOnlyField(source="recipe.cooking_time")

    class Meta:
        model = ShoppingCartRecipe
        fields = ("id", "name", "image", "cooking_time")

    def validate(self, data):
        recipe_id = self.context["view"].kwargs.get("recipe_id")
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if ShoppingCartRecipe.objects.filter(
            user=self.context["request"].user, recipe=recipe
        ).exists():
            raise serializers.ValidationError({"errors": _(RE_SUBSCRIBTION_ERROR)})
        return data
