import re

from django.core.exceptions import ValidationError


def validate_hex_code(value):
    if not re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", value):
        raise ValidationError(f"{value} не является HEX-кодом")


def validate_nonzero(value):
    if value == 0:
        raise ValidationError("Число должно быть больше 0")
