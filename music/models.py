from django.db import models
from .validators import validate_file_extension, validate_file_size


class Song(models.Model):
    name = models.CharField(max_length=200, unique=True)
    songfile = models.FileField(upload_to='songs', max_length=200, validators=[validate_file_extension,
                                                                               validate_file_size])

    def __str__(self):
        return self.name
