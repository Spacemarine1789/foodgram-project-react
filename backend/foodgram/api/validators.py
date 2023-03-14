from django.core.exceptions import ValidationError


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
