from rest_framework import filters


class RecipeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        is_favorited = request.query_params.get("is_favorited")
        is_in_shopping_cart = request.query_params.get("is_in_shopping_cart")
        author_id = request.query_params.get("author")
        tags = request.query_params.getlist("tags")
        if author_id:
            queryset = queryset.filter(author__id=author_id)
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        if not request.user.is_authenticated:
            return queryset
        if is_favorited:
            queryset = queryset.filter(favorite_for__user=request.user)
        if is_in_shopping_cart:
            queryset = queryset.filter(in_shopping_carts__user=request.user)
        return queryset


class IngredientSearchFilter(filters.SearchFilter):
    search_param = "name"
