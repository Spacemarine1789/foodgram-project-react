from string import hexdigits

from django.core.exceptions import ValidationError


def hex_color_validator(color: str) -> str:
    """Check color against hexadecimal system"""

    color = color.strip(' #')
    if len(color) not in (3, 6):
        raise ValidationError(
            f'Code {color} are not correct length ({len(color)}).'
        )
    if not set(color).issubset(hexdigits):
        raise ValidationError(
            f'{color} are not HEX.'
        )
    if len(color) == 3:
        return f'#{color[0] * 2}{color[1] * 2}{color[2] * 2}'.upper()
    return '#' + color.upper()


def tags_exist_validator(tags_ids, Tag) -> None:
    """Check existing tags with specified tags_ids"""

    exists_tags = Tag.objects.filter(id__in=tags_ids)
    if len(exists_tags) != len(tags_ids):
        raise ValidationError('Указан несуществующий тэг')


def ingredients_exist_validator(ingredients, Ingredient):
    """Check existing ingredients with specified ingredients_ids"""

    ings_ids = [None] * len(ingredients)

    for idx, ing in enumerate(ingredients):
        ingredients[idx]['amount'] = int(ingredients[idx]['amount'])
        if ingredients[idx]['amount'] < 1:
            raise ValidationError('Неправильное количество ингидиента')
        ings_ids[idx] = ing.pop('id', 0)

    ings_in_db = Ingredient.objects.filter(id__in=ings_ids).order_by('pk')
    ings_ids.sort()

    for idx, id in enumerate(ings_ids):
        ingredient: 'Ingredient' = ings_in_db[idx]
        if ingredient.id != id:
            raise ValidationError('Ингридент не существует')

        ingredients[idx]['ingredient'] = ingredient
    return ingredients
