from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCartRecipe, Tag)
from users.models import Subscription

from .filters import RecipeFilterBackend
from .generics import CreateDeleteAPIView
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeSerializer, ShoppingCartSerializer,
                          SubscribeSerializer, TagSerializer)

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (RecipeFilterBackend,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SubscribeApiView(CreateDeleteAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer

    def perform_create(self, serializer):
        subscribed_to = get_object_or_404(User, pk=self.kwargs.get("user_id"))
        serializer.save(
            subscriber=self.request.user, subscribed_to=subscribed_to)

    def delete(self, request, *args, **kwargs):
        subscribed_to = get_object_or_404(User, pk=self.kwargs.get("user_id"))
        try:
            instance = get_object_or_404(
                Subscription,
                subscriber=self.request.user,
                subscribed_to=subscribed_to
            )
        except Http404:
            return Response(
                {"errors": "Рецепт не добавлен в избранное"},
                status.HTTP_400_BAD_REQUEST,
            )
        super().perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeListApiView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return self.request.user.subscribed_to.all()


class FavoriteApiView(CreateDeleteAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get("recipe_id"))
        serializer.save(user=self.request.user, recipe=recipe)

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get("recipe_id"))
        try:
            instance = get_object_or_404(
                Favorite, user=self.request.user, recipe=recipe
            )
        except Http404:
            return Response(
                {"errors": "Рецепт не добавлен в избранное"},
                status.HTTP_400_BAD_REQUEST,
            )
        super().perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartApiView(CreateDeleteAPIView):
    queryset = ShoppingCartRecipe.objects.all()
    serializer_class = ShoppingCartSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get("recipe_id"))
        serializer.save(user=self.request.user, recipe=recipe)

    def delete(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get("recipe_id"))
        try:
            instance = get_object_or_404(
                ShoppingCartRecipe, user=self.request.user, recipe=recipe
            )
        except Http404:
            return Response(
                {"errors": "Рецепт не добавлен в список покупок"},
                status.HTTP_400_BAD_REQUEST,
            )
        super().perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def download_shopping_cart(request):
    listi = (
        IngredientRecipe.objects.filter(
            recipe__in_shopping_carts__user=request.user)
        .values("ingredient__name")
        .annotate(num=Sum("amount"))
    )
    content = "\n".join(
        f" - {name.title()} ({measurement_unit}) -> {num} "
        for name, num, measurement_unit in listi.values_list(
            "ingredient__name", "num", "ingredient__measurement_unit"
        )
    )
    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=shopping_list.txt"
    return response
