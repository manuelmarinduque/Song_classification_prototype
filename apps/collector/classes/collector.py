import spotipy
from statistics import quantiles

from apps.collector.models import Artist, Album, Song
from django.db.utils import IntegrityError


class Collector():

    def __init__(self, artist_id):
        self.artist_id = artist_id
        self.connection = self.__getAccessSpotify()

    def __getAccessSpotify(self):
        credentials = spotipy.SpotifyClientCredentials(
            '55c64375790e42f298941e9bdd0dbbc0', '47744189d3844da0a5f57aada4747d79')
        token = credentials.get_access_token()
        connection = spotipy.Spotify(auth=token)
        return connection

    def getArtistObject(self, dict_artist_info):
        artist_info = {'identifier': self.artist_id,
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
        artist_albums_info1 = self.connection.artist_albums(self.artist_id, 'album', 'CO', 50)
        artist_albums1 = artist_albums_info1.get('items')
        artist_albums_info2 = self.connection.artist_albums(self.artist_id, 'single', 'CO', 50)
        artist_albums2= artist_albums_info2.get('items')
        artist_albums = artist_albums1 + artist_albums2
        for album in artist_albums:
            album_name = album.get('name').lower()
            included_words = self.__validationIncludedWords(album_name, 'album')
            if not included_words:
                album_id = album.get('id')
                album_popularity = self.__getPopularity(album_id, 'album')
                if album_popularity >= 0:
                    album_year = album.get('release_date')[0:4]
                    album_info = {'name': album_name,
                                  'identifier': album_id,
                                  'artist': artist_object,
                                  'popularity': album_popularity,
                                  'year': album_year}
                    album_object = Album(**album_info)
                    try:
                        album_object.save()
                    except IntegrityError:
                        continue
                    else:
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
            # Para los singles eliminar las palabras 'remix', 'version', 'versión'.
            avoid_words = ('live', 'en vivo', 'mtv', '(vivo)',
                           'instrumental', 'interludio', 'en directo', 'commentary')
        else:
            avoid_words = ('homenaje', 'gira', 'tour', 'live', 'mtv', 'commentary',
                           'en vivo', 'plug', 'unplugged', 'concierto', 'concert', 'track by track',
                           'primera fila', 'pistas', 'sinfónico', 'en directo')
        for word in avoid_words:
            if element_name.find(word) != -1:
                var = True
        return var

    def __getAlbumSongs(self, album_object):
        album_songs_info = self.connection.album_tracks(album_object.identifier, market='CO')
        album_songs = album_songs_info.get('items')
        for song in album_songs:
            song_name = song.get('name').lower()
            in_database = Song.objects.filter(name=song_name,
                                              album__artist__identifier=self.artist_id).exists()
            if not in_database:
                included_words = self.__validationIncludedWords(song_name, 'song')
                if not included_words:
                    song_id = song.get('id')
                    song_popularity = self.__getPopularity(song_id, 'song')
                    song_info = self.__getAudioFeatures(song_id, song_name,
                                                        song_popularity, album_object)
                    song_object = Song(**song_info)
                    try:
                        song_object.save()
                    except IntegrityError:
                        continue
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
        atributes_not_included = ('type', 'uri', 'track_href',
                                  'analysis_url', 'id')
        song_atributes = {}
        for key, value in dict_song_description.items():
            if key not in atributes_not_included:
                song_atributes[key] = value
        return song_atributes
