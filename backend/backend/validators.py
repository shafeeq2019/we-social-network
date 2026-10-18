from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_image_size(image):
    if image.size > MAX_IMAGE_SIZE:
        raise ValidationError('The image must not be larger than 5 MB.', code='file_too_large')


# Used together with forms.ImageField, which additionally checks with Pillow
# that the file really is an image
IMAGE_VALIDATORS = [
    FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp']),
    validate_image_size,
]
