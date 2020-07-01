from django.shortcuts import render

def index(request):
    return render(request, 'album/index.html')

def albums(request):
    return render(request, 'album/beauty_album.html')

def classic(request):
    return render(request, 'album/classic.html')