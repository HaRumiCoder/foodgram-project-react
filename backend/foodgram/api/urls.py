from django.urls import include, path
from api.views import FavoriteApiView, IngredientViewSet, RecipeViewSet, TagViewSet, ShoppingCartApiView
from rest_framework.routers import SimpleRouter
from api.views import SubscribeApiView, SubscribeListApiView, download_shopping_cart

router_v1 = SimpleRouter()
router_v1.register("tags", TagViewSet)
router_v1.register("ingredients", IngredientViewSet)
router_v1.register("recipes", RecipeViewSet)

urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("users/subscriptions/", SubscribeListApiView.as_view()),
    path("users/<int:user_id>/subscribe/", SubscribeApiView.as_view()),
    path("recipes/<int:recipe_id>/favorite/", FavoriteApiView.as_view()),
    path("recipes/<int:recipe_id>/shopping_cart/", ShoppingCartApiView.as_view()),
    path("recipes/download_shopping_cart/", download_shopping_cart),
    path("", include("djoser.urls")),
    path("", include(router_v1.urls)),
]
