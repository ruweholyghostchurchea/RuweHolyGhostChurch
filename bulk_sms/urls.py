
from django.urls import path
from . import views

app_name = 'bulk_sms'

urlpatterns = [
    path('', views.index, name='index'),
]
