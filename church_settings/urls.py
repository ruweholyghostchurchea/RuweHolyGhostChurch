
from django.urls import path
from . import views

app_name = 'church_settings'

urlpatterns = [
    path('', views.index, name='index'),
]
