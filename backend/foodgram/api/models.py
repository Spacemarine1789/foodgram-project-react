from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.TextField(
        verbose_name='Тег',
    )
    color = models.CharField(max_length=10)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = [
            models.UniqueConstraint(
                fields=['slug', 'color'],
                name='unique_tag'
            )
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.TextField(
        verbose_name='Ингредиент',
    )
    measurement_unit = models.CharField(
        max_length=100,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    name = models.CharField(
        max_length=200, verbose_name='Рецепт',
    )
    image = models.ImageField(
        upload_to='recipes/', blank=True, null=True,
    )
    text = models.TextField(
        blank=True, null=True, verbose_name='Текст',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        blank=True,
        null=True,
        verbose_name='Ингридиент',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=True,
        null=True,
        verbose_name='Тег',
    )
    cooking_time = models.IntegerField(
        verbose_name='Длительность',
        validators=[MinValueValidator(0)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='amount'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='amount'
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'


class ShoppingCartRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Рецепт в корзине для покупок'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite',
    )

    class Meta:
        verbose_name = 'Рецепт в списке избраных'


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
    )

    class Meta:
        verbose_name = 'Автор в списке отслеживыемых'
