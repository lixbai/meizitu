from django.shortcuts import render

def index(request):
    return render(request, 'album/index.html')

def albums(request):
    return render(request, 'album/beauty_album.html')

def album_detail(request, album_id):
    return render(request, 'album/pic_show.html')