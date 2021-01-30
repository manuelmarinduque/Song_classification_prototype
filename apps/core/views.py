from django.views.generic import RedirectView, TemplateView
from classes.collector import Collector
from social_django.models import UserSocialAuth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.


# Variable global que almacena el dataframe con las canciones clasificadas por emociones, de esta
# forma se evita almacenar en la BD las canciones de un usuario o generar un csv para luego leerlo
# al crear la playlist en la cuenta del usuario.
# El servidor no se puede reiniciar porque también reinicia a 'None' el valor de la variable global,
# lo cual lo hace susceptible a fallos. Si se reinicia se deben generar las playlist nuevamente.
data_frame_global = None


class LoginView(TemplateView):
    template_name = 'core/login.html'
    http_method_names = ['get']
    
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
        data_frame = collector.readSavedTracks()
        data_frame_pred = collector.modelPredicts(data_frame)
        global data_frame_global
        data_frame_global = data_frame_pred
        data_frame_pred = data_frame_pred.drop(['track_id', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'tempo', 'valence', 'liveness', 'speechiness'], axis=1)
        self.extra_context = {'relax_songs': data_frame_pred[data_frame_pred.emotion == 0].values,
                              'happy_songs': data_frame_pred[data_frame_pred.emotion == 1].values,
                              'sad_songs': data_frame_pred[data_frame_pred.emotion == 2].values}
        # La ejecución del método debe continuar con normalidad.
        return super().get(request, *args, **kwargs)
    
class CreateSelectedPlaylist(LoginRequiredMixin, RedirectView):
    http_method_names = ['get']
    url = reverse_lazy('core:playlist_page_confirmation', args=('ok',))

    def get(self, request, *args, **kwargs):
        token = UserSocialAuth.objects.get(user=request.user.id).extra_data.get('access_token')
        collector = Collector('null', token, request.user)
        playlist_value = self.kwargs.get('playlist_value')
        global data_frame_global
        if playlist_value == '1':
            collector.createPlaylist('Momentos felices', data_frame_global[data_frame_global.emotion == 1].track_id.values)
            print(len(data_frame_global[data_frame_global.emotion == 1].track_id.values))
        elif playlist_value == '2':
            collector.createPlaylist('Momentos de relajación', data_frame_global[data_frame_global.emotion == 0].track_id.values)
            print(len(data_frame_global[data_frame_global.emotion == 0].track_id.values))
        elif playlist_value == '3':
            collector.createPlaylist('Momentos tristes', data_frame_global[data_frame_global.emotion == 2].track_id.values)
            print(len(data_frame_global[data_frame_global.emotion == 2].track_id.values))
        return super().get(request, *args, **kwargs)
