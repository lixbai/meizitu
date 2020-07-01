from django.shortcuts import render

# Create your views here.
def news_list(request):
    print('news_list')
    return render(request, 'news/news_list.html')

def news_detail(request, news_id):
    return render(request, 'news/news_detail.html')