from rest_framework import filters


class RecipeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        is_favorited = request.query_params.get("is_favorited")
        is_in_shopping_cart = request.query_params.get("is_in_shopping_cart")
        author = request.query_params.get("author")
        tags = request.query_params.getlist("tags")
        if is_favorited:
            queryset = queryset.filter(favorite_for__user=request.user)
        if is_in_shopping_cart:
            queryset = queryset.filter(in_shopping_carts__user=request.user)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if tags:
            queryset = queryset.filter(tags__id__in=tags)
        return queryset
