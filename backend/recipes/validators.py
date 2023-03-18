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
