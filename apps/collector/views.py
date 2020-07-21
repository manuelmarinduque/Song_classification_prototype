from django.shortcuts import render

# Create your views here.


def search_artist(request):
    return render(request, 'collector/search_artist.html')
