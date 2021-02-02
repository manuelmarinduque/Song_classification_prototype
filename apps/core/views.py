from django.views.generic import RedirectView, TemplateView
from social_django.models import UserSocialAuth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

from spotipy.exceptions import SpotifyException
from classes.collector import Collector
from pandas import read_csv


# Create your views here.


class LoginView(TemplateView):
    template_name = 'core/login.html'
    http_method_names = ['get']

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('core:home_page')
        return super().dispatch(request, *args, **kwargs)
    
    
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/home.html'
    http_method_names = ['get']

class GeneratePlaylistView(LoginRequiredMixin, TemplateView):
    template_name = 'core/playlist.html'
    http_method_names = ['get']

    # Aplicando la regla Heredar, Sobreescribir y Continuar ejecución.
    def get(self, request, *args, **kwargs):
        # Se sobrescribe este método para adaptar la clase TemplateView a una necesidad específica. 
        token = UserSocialAuth.objects.get(user=request.user.id).extra_data.get('access_token')
        collector = Collector('null', token, request.user)
        try:
            data_frame = collector.readSavedTracks()
            data_frame_pred = collector.modelPredicts(data_frame)
        except SpotifyException:
            messages.error(request, 'Su sesión ha expirado. Inicia sesión nuevamente.')
            return redirect('logout')
        # TODO ¿utilizar la sesión del usuario? Esto mediante el diccionario request.session. Leer sobre sessión en la documentación.
        data_frame_pred.to_csv('apps/core/data/data_frame_pred.csv', index=False)
        data_frame_pred = data_frame_pred.drop(['track_id', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'tempo', 'valence', 'liveness', 'speechiness'], axis=1)
        self.extra_context = {'relax_songs': data_frame_pred[data_frame_pred.emotion == 0].values,
                              'happy_songs': data_frame_pred[data_frame_pred.emotion == 1].values,
                              'sad_songs': data_frame_pred[data_frame_pred.emotion == 2].values}
        # La ejecución del método debe continuar con normalidad.
        return super().get(request, *args, **kwargs)
    
class CreateSelectedPlaylist(LoginRequiredMixin, RedirectView):
    http_method_names = ['get']
    url = reverse_lazy('core:playlist_confirmation_page', args=('ok',))

    def get(self, request, *args, **kwargs):
        token = UserSocialAuth.objects.get(user=request.user.id).extra_data.get('access_token')
        collector = Collector('null', token, request.user)
        playlist_value = self.kwargs.get('playlist_value')
        dataframe = read_csv('apps/core/data/data_frame_pred.csv')
        if playlist_value == '1':
            collector.createPlaylist('Momentos felices', dataframe[dataframe.emotion == 1].track_id.values)
        elif playlist_value == '2':
            collector.createPlaylist('Momentos de relajación', dataframe[dataframe.emotion == 0].track_id.values)
        elif playlist_value == '3':
            collector.createPlaylist('Momentos tristes', dataframe[dataframe.emotion == 2].track_id.values)
        return super().get(request, *args, **kwargs)
