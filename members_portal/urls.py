from django.urls import path
from . import views

app_name = 'members_portal'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('my-church/', views.my_church, name='my_church'),
    path('my-pastorate/', views.my_pastorate, name='my_pastorate'),
    path('my-diocese/', views.my_diocese, name='my_diocese'),
    path('my-headquarters/', views.my_headquarters, name='my_headquarters'),
    path('attendance/', views.attendance, name='attendance'),
    path('giving/', views.giving, name='giving'),
]
