from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.utils import IntegrityError

from .classes.collector import Collector
from spotipy.exceptions import SpotifyException
from .models import Artist, Song

# Create your views here.


def searchArtist(request):
    if request.method == 'POST':
        artist_uri = request.POST.get('artist_uri')
        return HttpResponseRedirect(reverse('collector:add_database_page', args=(artist_uri, )))
    else:
        songs_remastered = Song.objects.filter(name__contains = 'remast')
        # for song in songs_remastered:
        #     element = song.name.partition(' (')[0]
        #     song.name = element
        #     song.save()
        return render(request, 'collector/search_artist.html')


def addDatabase(request, artist_uri):
    collector = Collector()
    for artist_id in artists:
        artist_object = collector.getArtistObject(artist_id)
        collector.getArtistAlbums(artist_object)
    return render(request, 'collector/search_artist.html', {'message': 'ok'})
