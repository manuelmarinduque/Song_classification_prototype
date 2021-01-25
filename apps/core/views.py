from django.views.generic import TemplateView
from classes.collector import Collector
from social_django.models import UserSocialAuth

# Create your views here.


class LoginView(TemplateView):
    template_name = 'core/login.html'
    http_method_names = ['get']
    
class HomeView(TemplateView):
    template_name = 'core/home.html'
    http_method_names = ['get']

class GeneratePlaylistView(TemplateView):
    template_name = 'core/playlist.html'
    http_method_names = ['get']

    # Aplicando la regla Heredar, Sobreescribir y Continuar ejecución.
    def get(self, request, *args, **kwargs):
        # Se sobrescribe este método para adaptar la clase TemplateView a una necesidad específica. 
        token = UserSocialAuth.objects.get(user=request.user.id).extra_data.get('access_token')
        collector = Collector('null', token, request.user)
        data_frame = collector.readSavedTracks()
        data_frame_pred = collector.modelPredicts(data_frame)
        data_frame_pred = data_frame_pred.drop(['track_id', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'loudness', 'tempo', 'valence', 'liveness', 'speechiness'], axis=1)
        self.extra_context = {'relax_songs': data_frame_pred[data_frame_pred.emotion == 0].values,
                              'happy_songs': data_frame_pred[data_frame_pred.emotion == 1].values,
                              'sad_songs': data_frame_pred[data_frame_pred.emotion == 2].values}
        # La ejecución del método debe continuar con normalidad.
        return super().get(request, *args, **kwargs)
