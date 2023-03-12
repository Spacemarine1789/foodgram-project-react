from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .validators import hex_color_validator

MAX_LEN_CHARFILD = 64
MAX_COOKING_TIME = 3600
MAX_AMOUNT = 128


class User(AbstractUser):

    first_name = models.CharField(verbose_name='first name', max_length=256)
    last_name = models.CharField(verbose_name='last name', max_length=256)
    email = models.EmailField(verbose_name='email address', max_length=256, unique=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


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
        max_length=MAX_LEN_CHARFILD,
        verbose_name='Ингредиент',
    )
    measurement_unit = models.CharField(
        max_length=32,
        verbose_name='Единица измерения'
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
        Ingredient,
        related_name='recipes',
        verbose_name='Ингридиент',
        through='api.RecipeIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег',
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

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_amount'
            )
        ]


class ShoppingCartRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_cart',
    )

    class Meta:
        verbose_name = 'Рецепт в корзине для покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_cart'
            )
        ]


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite',
    )

    class Meta:
        verbose_name = 'Рецепт в списке избраных'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            )
        ]


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
    )

    class Meta:
        verbose_name = 'Автор в списке отслеживыемых'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]
