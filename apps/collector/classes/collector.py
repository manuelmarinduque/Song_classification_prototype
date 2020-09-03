import spotipy
from statistics import quantiles

from apps.collector.models import Artist, Album, Song
from django.db.utils import IntegrityError


class Collector():

    def __init__(self):
        self.connection = self.__getAccessSpotify()

    def __getAccessSpotify(self):
        credentials = spotipy.SpotifyClientCredentials('55c64375790e42f298941e9bdd0dbbc0', '47744189d3844da0a5f57aada4747d79')
        token = credentials.get_access_token()
        connection = spotipy.Spotify(auth=token)
        return connection

    def getArtistObject(self, artist_id):
        dict_artist_info = self.connection.artist(artist_id)
        artist_info = {'identifier': dict_artist_info.get('id'),
                       'name': dict_artist_info.get('name'),
                       'popularity': dict_artist_info.get('popularity'),
                       'followers': dict_artist_info.get('followers').get('total')}
        artist_object = Artist(**artist_info)
        artist_object.save()
        return artist_object

    def getArtistAlbums(self, artist_object):
        for album_object in self.__getArtistAlbumsInformation(artist_object):
            self.__getAlbumSongs(album_object)

    def __getArtistAlbumsInformation(self, artist_object):
        artist_albums_50 = self.connection.artist_albums(artist_object.identifier, 'album', 'CO', 50)
        artist_singles = self.connection.artist_albums(artist_object.identifier, 'single', 'CO', 50)
        artist_catalog_info = artist_albums_50.get('items') + artist_singles.get('items')
        if len(artist_albums_50) >= 49:
            artist_albums_100 = self.connection.artist_albums(artist_object.identifier, 'album', 'CO', 50, 50)
            artist_catalog_info = artist_catalog_info + artist_albums_100.get('items')
        for album in artist_catalog_info:
            album_id = album.get('id')
            in_database = Album.objects.filter(identifier=album_id).exists()
            if not in_database:
                album_name = album.get('name').lower()
                included_words = self.__validationIncludedWords(album_name, 'album')
                if not included_words:
                    album_popularity = self.__getPopularity(album_id, 'album')
                    album_year = album.get('release_date')[0:4]
                    album_info = {'name': album_name,
                                  'identifier': album_id,
                                  'artist': artist_object,
                                  'popularity': album_popularity,
                                  'year': album_year}
                    album_object = Album(**album_info)
                    album_object.save()
                    yield album_object

    def __getPopularity(self, identifier, type_of):
        if type_of == 'song':
            dict_info = self.connection.track(identifier)
        else:
            dict_info = self.connection.album(identifier)
        popularity = dict_info.get('popularity')
        return popularity

    def __validationIncludedWords(self, element_name, type_of):
        var = False
        if type_of == 'song':
            avoid_words = ('- live', 'en vivo', '- vivo', 'en directo', '- directo')
        else:
            avoid_words = ('homenaje', 'tributo', 'live', 'mtv', 'commentary', 'en vivo', 
                           'plug', 'unplugged', 'concierto', 'concert', 'track by track', 
                           'primera fila', 'sinfónico', 'en directo', 'navidad')
        for word in avoid_words:
            if element_name.find(word) != -1:
                var = True
        return var

    def __getAlbumSongs(self, album_object):
        album_songs_50 = self.connection.album_tracks(album_object.identifier, market='CO')
        album_songs = album_songs_50.get('items')
        if len(album_songs) >= 49:
            album_songs_100 = self.connection.album_tracks(album_object.identifier, market='CO', offset=50)
            album_songs = album_songs + album_songs_100.get('items')         
        for song in album_songs:
            song_id = song.get('id')
            in_database = Song.objects.filter(identifier=song_id).exists()
            if not in_database:
                song_name = song.get('name').lower()
                included_words = self.__validationIncludedWords(song_name, 'song')
                if not included_words:
                    song_popularity = self.__getPopularity(song_id, 'song')
                    song_info = self.__getAudioFeatures(song_id, song_name, song_popularity, album_object)
                    song_object = Song(**song_info)
                    song_object.save()
                    # print(song_object.album.artist.name)

    def __getAudioFeatures(self, song_id, song_name, song_popularity, album_object):
        dict_song_description = self.connection.audio_features(song_id)[0]
        song_audio_features = self.__getSongAtributes(dict_song_description)
        song_audio_features['identifier'] = song_id
        song_audio_features['name'] = song_name
        song_audio_features['popularity'] = song_popularity
        song_audio_features['album'] = album_object
        return song_audio_features

    def __getSongAtributes(self, dict_song_description):
        atributes_not_included = ('type', 'uri', 'track_href', 'analysis_url', 'id')
        song_atributes = {}
        for key, value in dict_song_description.items():
            if key not in atributes_not_included:
                song_atributes[key] = value
        return song_atributes
