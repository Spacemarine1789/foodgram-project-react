from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    FavoriteRecipe, Follow, Ingredient, Recipe, RecipeIngredient,
    ShoppingCartRecipe, Tag, User,
)


class CustomAdmin(UserAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    list_editable = ('name', 'color', 'slug',)
    search_fields = ('name', 'color', 'slug',)
    list_filter = ('name', 'color', 'slug',)
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    list_editable = ('name', 'measurement_unit',)
    search_fields = ('name', 'measurement_unit',)
    list_filter = ('name', 'measurement_unit',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'name', 'text', 'cooking_time', 'pub_date',
    )
    list_editable = ('author', 'name', 'text', 'cooking_time',)
    search_fields = (
        'id', 'author', 'name', 'text', 'cooking_time', 'pub_date',
    )
    list_filter = (
        'id', 'author', 'name', 'text', 'cooking_time', 'pub_date',
    )
    empty_value_display = '-пусто-'


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount',)
    list_editable = ('recipe', 'ingredient', 'amount',)
    search_fields = ('recipe', 'ingredient',)
    list_filter = ('recipe', 'ingredient',)
    empty_value_display = '-пусто-'


class ShoppingCartRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    list_editable = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-пусто-'


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    list_editable = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author',)
    list_editable = ('user', 'author',)
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author',)
    empty_value_display = '-пусто-'


admin.site.register(User, CustomAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(ShoppingCartRecipe, ShoppingCartRecipeAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(Follow, FollowAdmin)
