from django.urls import path
from . import views

app_name = 'public_site'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.events, name='events'),
    path('donation/', views.donation, name='donation'),
]
