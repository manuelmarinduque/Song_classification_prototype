from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.utils import IntegrityError

from .models import Artist, Album, Song
from .classes.collector import Collector
from spotipy.exceptions import SpotifyException

# Create your views here.


def searchArtist(request):
    if request.method == 'POST':
        artist_uri = request.POST.get('artist_uri')
        return HttpResponseRedirect(reverse('collector:add_database_page', args=(artist_uri,)))
    else:
        return render(request, 'collector/search_artist.html')


def addDatabase(request, artist_uri):
    collector = Collector(artist_uri)
    try:
        dict_artist_info = collector.connection.artist(artist_uri)
    except SpotifyException:
        return HttpResponseRedirect(reverse('collector:search_artist_page') + '?fail')
    else:
        artist_info = collector.getArtistInformation(dict_artist_info)
        collector.getArtistAlbums(artist_info)
        return HttpResponse(f'ok')