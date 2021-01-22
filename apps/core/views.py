from django.shortcuts import render
from classes.collector import Collector
from social_django.models import UserSocialAuth

# Create your views here.


def login(request):
    return render(request, 'core/login.html')

def home(request):
    return render(request, 'core/home.html')

def generatePlaylist(request):
    token = UserSocialAuth.objects.get(user=request.user.id).extra_data.get('access_token')
    collector = Collector('null', token, request.user)
    data_frame = collector.readSavedTracks()
    return render(request, 'core/playlist.html')
