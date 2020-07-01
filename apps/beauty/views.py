from django.shortcuts import render

def index(request):
    return render(request, 'beauty/beauty.html')

def beauty_detail(request, beauty_id):
    return render(request, 'beauty/beauty_detail.html')