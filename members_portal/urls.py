from django.urls import path
from . import views

app_name = 'members_portal'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('attendance/', views.attendance, name='attendance'),
    path('giving/', views.giving, name='giving'),
]
