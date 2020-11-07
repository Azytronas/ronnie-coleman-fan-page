from django.shortcuts import get_object_or_404, render
from .models import Song
from .forms import SongForm


def index(request):
    song_list = Song.objects.all()
    if request.method == "POST":
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            success_message = "Successfully uploaded!"
            context = {'form': form, 'song_list': song_list, 'success_message': success_message}
            return render(request, 'music/index.html', context)
    else:
        form = SongForm()
    context = {'song_list': song_list, 'form': form}
    return render(request, 'music/index.html', context)


def details(request, song_name):
    song = get_object_or_404(Song, name=song_name)
    context = {'song': song}
    return render(request, 'music/details.html', context)
