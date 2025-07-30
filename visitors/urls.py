
from django.urls import path
from . import views

app_name = 'visitors'

urlpatterns = [
    path('', views.index, name='index'),
]
