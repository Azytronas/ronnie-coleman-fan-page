from django.test import TestCase
from .models import Song


class SongModelTest(TestCase):

    def test_duplicate_names(self):
        no_dupes = True
        try:
            for song in Song.objects.all():
                print(song.name)
        except Song.MultipleObjectsReturned:
            no_dupes = False
        self.assertIs(no_dupes, True)
