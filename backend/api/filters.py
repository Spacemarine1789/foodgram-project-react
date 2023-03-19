from django.shortcuts import get_object_or_404
from rest_framework import filters, exceptions
from recipes.models import Recipe, Tag
from users.models import User


class IsFavoritedFilterBackend(filters.BaseFilterBackend):
    """
    Backend for filtering recipes by they M2M relation with
    FavoriteRecipe Model
    """
    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('is_favorited', '0') == '1':
            if request.user.is_anonymous:
                raise exceptions.ValidationError
            return Recipe.objects.filter(favorite__user=request.user)
        return queryset


class IsInShoppingCartFilterBackend(filters.BaseFilterBackend):
    """
    Backend for filtering recipes by they M2M relation with
    ShoppingCartRecipe Model
    """
    def filter_queryset(self, request, queryset, view):
        if request.query_params.get('is_in_shopping_cart', '0') == '1':
            if request.user.is_anonymous:
                raise exceptions.ValidationError
            shopping_cart = request.user.shopping_cart.all()
            return Recipe.objects.filter(shopping_cart__in=shopping_cart)
        return queryset


class AuthorListFilterBackend(filters.BaseFilterBackend):
    """
    Backend for filtering recipes author by id field
    """
    def filter_queryset(self, request, queryset, view):
        author_id = request.query_params.get('author', None)
        if author_id is None:
            return queryset
        author = get_object_or_404(User, id=author_id)
        return author.recipes.all()


class TagListFilterBackend(filters.BaseFilterBackend):
    """
    Backend for filtering recipes tags by slug field
    """
    def filter_queryset(self, request, queryset, view):
        tag_slug = request.query_params.getlist('tags')
        if len(tag_slug) == 0:
            return queryset
        return Recipe.objects.filter(tags__slug__in=tag_slug).distinct()
