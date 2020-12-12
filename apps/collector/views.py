from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.utils import IntegrityError

from .classes.collector import Collector
from spotipy.exceptions import SpotifyException
from .models import Artist, Song
from social_django.models import UserSocialAuth

# Create your views here.


def searchArtist(request):
    if request.method == 'POST':
        artist_uri = request.POST.get('artist_uri')
        return HttpResponseRedirect(reverse('collector:add_database_page', args=(artist_uri, )))
    else:
        return render(request, 'collector/search_artist.html')


def addDatabase(request, artist_uri):
    artist_id = artist_uri[15:]
    token = UserSocialAuth.objects.get(user=request.user.id).extra_data.get('access_token')
    collector = Collector(artist_id, token, request.user)
    try:
        dict_artist_info = collector.connection.artist(artist_id)
    except SpotifyException:
        return HttpResponseRedirect(reverse('collector:search_artist_page') + '?fail')
    else:
        exist_artist = Artist.objects.filter(identifier=artist_id).exists()
        if exist_artist:
            return HttpResponseRedirect(reverse('collector:search_artist_page') + '?exist')
        else:
            artist_object = collector.getArtistObject(dict_artist_info)
            collector.getArtistAlbums(artist_object)
            counter_artist_songs = Song.objects.filter(album__artist__identifier=artist_id).count()
            return render(request, 'collector/search_artist.html', {
                'counter': counter_artist_songs,
            })
