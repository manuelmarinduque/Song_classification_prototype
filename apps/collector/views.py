from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.utils import IntegrityError

# from .classes.collector import Collector
from spotipy.exceptions import SpotifyException
from .models import SongsCatalogue

import csv

# Create your views here.


def searchArtist(request):
    if request.method == 'POST':
        artist_uri = request.POST.get('artist_uri')
        return HttpResponseRedirect(reverse('collector:add_database_page', args=(artist_uri, )))
    else:
        # songs_remastered = Song.objects.filter(name__contains = 'remast')
        # for song in songs_remastered:
        #     element = song.name.partition(' (')[0]
        #     song.name = element
        #     song.save()
        return render(request, 'collector/search_artist.html')


def addDatabase(request, artist_uri):
    with open('apps/collector/Final_database.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')

        for line in csv_reader:
            song_object = SongsCatalogue(
                            name=line.get('name'),    
                            identifier=line.get('identifier'),
                            popularity=line.get('popularity'),
                            duration_ms=line.get('duration_ms'),
                            energy=line.get('energy'),
                            valence=line.get('valence'),
                            tempo=line.get('tempo'),
                            danceability=line.get('danceability'),
                            key=line.get('key'),
                            loudness=line.get('loudness'),
                            mode=line.get('mode'),
                            speechiness=line.get('speechiness'),
                            acousticness=line.get('acousticness'),
                            instrumentalness=line.get('instrumentalness'),
                            liveness=line.get('liveness'),
                            time_signature=line.get('time_signature'),
                            album_identifier=line.get('album_identifier'),
                            album_name=line.get('album_name'),
                            album_popularity=line.get('album_popularity'),
                            artist_identifier=line.get('artist_identifier'),
                            artist_name=line.get('artist_name')
                        )
            song_object.save()
