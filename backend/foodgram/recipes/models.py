from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from users.models import User
from .validators import hex_color_validator

MAX_LEN_CHARFILD = 64
MAX_COOKING_TIME = 3600
MAX_AMOUNT = 128


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Тег', max_length=MAX_LEN_CHARFILD, unique=True
    )
    color = models.CharField(max_length=7, unique=True)
    slug = models.SlugField(max_length=MAX_LEN_CHARFILD, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def clean(self) -> None:
        self.color = hex_color_validator(self.color)
        return super().clean()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=MAX_LEN_CHARFILD, verbose_name='Ингредиент',
    )
    measurement_unit = models.CharField(
        max_length=32, verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            ),
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    name = models.CharField(
        max_length=MAX_LEN_CHARFILD, verbose_name='Название',
    )
    image = models.ImageField(
        upload_to='recipes/', max_length=5000,
    )
    text = models.TextField(verbose_name='Текст',)
    ingredients = models.ManyToManyField(
        Ingredient, related_name='recipes', verbose_name='Ингридиент',
        through='api.RecipeIngredient',
    )
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='Тег',
    )
    cooking_time = models.IntegerField(
        verbose_name='Длительность',
        validators=[MinValueValidator(0), MaxValueValidator(MAX_COOKING_TIME)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='amount'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingamount'
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(0), MaxValueValidator(MAX_AMOUNT)]
    )
    add_date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_amount'
            )
        ]
        ordering = ('-add_date',)

    def __str__(self):
        return (
            f'В рецепте {self.recipe} содержится {self.ingredient}'
            f' в следующем количестве: {self.amount}'
        )


class ShoppingCartRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_cart',
    )
    add_date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт в корзине для покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_cart'
            )
        ]
        ordering = ('-add_date',)

    def __str__(self):
        return (
            f'Рецепт {self.recipe} находится в корзине'
            f' этого полльзователя {self.user}'
        )


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite',
    )
    add_date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт в списке избраных'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            )
        ]
        ordering = ('-add_date',)

    def __str__(self):
        return (
            f'Рецепт {self.recipe} находится в избраных'
            f' этого полльзователя {self.user}'
        )


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
    )
    add_date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Автор в списке отслеживыемых'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]
        ordering = ('-add_date',)

    def __str__(self):
        return (
            f'Автор {self.author} находится в отслеживаемых'
            f' этого полльзователя {self.user}'
        )
