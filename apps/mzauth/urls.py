from django.urls import path
from . import views
app_name = 'mzauth'

urlpatterns = [
    path('login/', views.login_view, name='login')
]