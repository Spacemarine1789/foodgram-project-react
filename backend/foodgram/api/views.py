from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import (HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST)
from .filters import (
    AuthorListFilterBackend, IsFavoritedFilterBackend,
    IsInShoppingCartFilterBackend,
)
from .mixins import add_del_act
from .models import (
    Ingredient, FavoriteRecipe, Follow, Recipe, ShoppingCartRecipe, Tag, User
)
from .permissions import IsStaffOrAuthorOrReadOnly
from .serializers import (
    IngredientSerializer, RecipeSerializer, TagSerializer,
    ShortRecipeSerializer, UserSubscribeSerializer
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class UserViewSet(DjoserUserViewSet):

    @action(methods=('GET',), detail=False)
    def subscriptions(self, request):
        if self.request.user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        pages = self.paginate_queryset(
            User.objects.filter(following__user=self.request.user)
        )
        serializer = UserSubscribeSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=('POST', 'DELETE'), detail=True)
    def subscribe(self, request, id):
        return add_del_act(
            request=request, id=id, model=Follow, query=User,
            ser=UserSubscribeSerializer
        )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsStaffOrAuthorOrReadOnly,)
    filter_backends = (
        AuthorListFilterBackend, IsFavoritedFilterBackend,
        IsInShoppingCartFilterBackend,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=('get',), detail=False)
    def download_shopping_cart(self, request):
        user = self.request.user
        if user.is_anonymous:
            raise ValidationError()
        if not user.shopping_cart.exists():
            mes = "You have no recipes in carts"
            return Response(data=mes, status=HTTP_400_BAD_REQUEST)
        filename = f'{user.username}_shopping_list.txt'
        shopping_list = [
            f'Список покупок для:\n\n{user.first_name} {user.last_name} \n'
        ]
        shopping_cart = request.user.shopping_cart.all()
        recipes = Recipe.objects.filter(shopping_cart__in=shopping_cart)
        amount = {}
        ing_ids = []
        for recipe in recipes:
            ingrediens = recipe.amount.all()
            for ing in ingrediens:
                if amount.get(f'{ing.ingredient.id}') is not None:
                    amount[f'{ing.ingredient.id}'] = (
                        amount.get(f'{ing.ingredient.id}') + ing.amount
                    )
                else:
                    ing_ids.append(ing.ingredient.id)
                    amount[f'{ing.ingredient.id}'] = ing.amount
        for i in ing_ids:
            ing = Ingredient.objects.get(id=i)
            am = amount[f'{i}']
            shopping_list.append(
                    f'{ing.name} ({ing.measurement_unit}) - {am}'
                )
        shopping_list.append('\nFoodgram')
        shopping_list = '\n'.join(shopping_list)
        response = HttpResponse(
            shopping_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(methods=('POST', 'DELETE'), detail=True)
    def shopping_cart(self, request, pk):
        return add_del_act(
            request=request, id=pk, model=ShoppingCartRecipe, query=Recipe,
            ser=ShortRecipeSerializer
        )

    @action(methods=('POST', 'DELETE'), detail=True)
    def favorite(self, request, pk):
        return add_del_act(
            request=request, id=pk, model=FavoriteRecipe, query=Recipe,
            ser=ShortRecipeSerializer
        )
