from django.forms import ModelForm
from music.models import Song


class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = ['name', 'songfile']
