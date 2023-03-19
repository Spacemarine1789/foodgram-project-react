import base64
from django.core.files.base import ContentFile
from django.db.models import F
from rest_framework import serializers
from recipes.models import (
    FavoriteRecipe, Follow, Ingredient, Recipe, RecipeIngredient,
    ShoppingCartRecipe, Tag
)
from users.models import User
from .validators import (
    amount_validator, tags_exist_validator,
    tags_ingredients_not_null_validator, unique_ingredients_validator,
    unique_tags_validator,
)


class UserSerializer(serializers.ModelSerializer):
    """"Alternate serializer for User model"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed',
        )
        read_only_fields = 'is_subscribed',

    def get_is_subscribed(self, obj):
        request = self.context['request']
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class Base64ImageField(serializers.ImageField):
    """"Field for images in base64 encoding"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class ShortRecipeSerializer(serializers.ModelSerializer):
    """"Alternate serializer for Recipe model read only"""
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'cooking_time',
        )
        read_only_fields = ('__all__',)


class UserSubscribeSerializer(UserSerializer):
    """"Serializer for User model in subscriptions endpoint"""
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )
        read_only_fields = '__all__',

    def get_is_subscribed(*args):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    """"Serializer for Tag model"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(serializers.ModelSerializer):
    """"Serializer for Ingredient model"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeSerializer(serializers.ModelSerializer):
    """"Serializer for Recipe model"""
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ('is_favorite', 'is_in_shopping_cart',)

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('ingamount__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        request = self.context['request']
        if request.user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        if request.user.is_anonymous:
            return False
        return ShoppingCartRecipe.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        tags_ingredients_not_null_validator(tags)
        tags_exist_validator(tags, Tag)
        unique_tags_validator(tags)
        tags_ingredients_not_null_validator(ingredients)
        unique_ingredients_validator(ingredients)
        amount_validator(ingredients)
        data.update({
            'ingredients': ingredients,
            'tags': tags
        })
        return data

    def create(self, validated_data: dict):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe_ingredients = []
        for ingredient in ingredients:
            recipe_ingredients.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=Ingredient.objects.get(
                        id=int(ingredient['id'])
                    ),
                    amount=int(ingredient['amount'])
                )
            )
        RecipeIngredient.objects.bulk_create(recipe_ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        for attr, value in validated_data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)

        if tags:
            instance.tags.clear()
            instance.tags.set(tags)

        if ingredients:
            instance.ingredients.clear()
            recipe_ingredients = []
            for ingredient in ingredients:
                recipe_ingredients.append(
                    RecipeIngredient(
                        recipe=instance,
                        ingredient=Ingredient.objects.get(
                            id=int(ingredient['id'])
                        ),
                        amount=int(ingredient['amount'])
                    )
                )
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

        return super().update(instance, validated_data)
