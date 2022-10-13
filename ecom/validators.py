from django.core.validators import ValidationError


def check_image(file):
    size = 500
    if file.size > size * 1024:
        raise ValidationError(f"File cannot be large than {size}KB!")
