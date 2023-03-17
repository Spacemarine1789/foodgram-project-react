from rest_framework.serializers import ValidationError
from recipes.models import MIN_AMOUNT, MAX_AMOUNT


def tags_exist_validator(tags_ids, Tag) -> None:
    """Check existing tags with specified tags_ids"""
    exists_tags = Tag.objects.filter(id__in=tags_ids)
    if len(exists_tags) != len(tags_ids):
        raise ValidationError('Указан несуществующий тег')


def tags_ingredients_not_null_validator(values):
    """Check that values exists in request"""
    if len(values) < 1:
        raise ValidationError('Добавьте хотя бы один ингредиент и тег.')
    return values


def unique_ingredients_validator(ingredients):
    """Check that ingredients in request are unique"""
    if len(ingredients) > len({item['id'] for item in ingredients}):
        raise ValidationError('Ингредиенты должны быть уникальные.')
    return ingredients


def unique_tags_validator(tags):
    """Check that tags in request are unique"""
    if len(tags) > len(set(tags)):
        raise ValidationError('Теги должны быть уникальные.')
    return tags


def amount_validator(ingredients):
    """Check amount of ingredients"""
    for item in ingredients:
        if int(item['amount']) < MIN_AMOUNT:
            raise ValidationError(
                f'Количество ингредиента должно быть больше {MIN_AMOUNT}'
            )
        if int(item['amount']) > MAX_AMOUNT:
            raise ValidationError(
                f'Количество ингредиента должно быть меньше {MAX_AMOUNT}'
            )
    return ingredients
