import os
from django.core.exceptions import ValidationError


def validate_file_extension(file):
    ext = os.path.splitext(file.name)[1]
    valid_extensions = ['.mp3']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Invalid file format (only upload .mp3 files).', code='0001')


def validate_file_size(file):
    if file.size > 15242880:
        raise ValidationError(
            'File size too big, max file size is 15 MB, given file size was: %(value)s MB',
            params={'value': (round(file.size/1048576, 2))})
