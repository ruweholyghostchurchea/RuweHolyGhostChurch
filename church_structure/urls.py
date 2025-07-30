
from django.urls import path
from . import views

app_name = 'church_structure'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/pastorates/<int:diocese_id>/', views.get_pastorates, name='get_pastorates'),
    path('api/churches/<int:pastorate_id>/', views.get_churches, name='get_churches'),
    path('diocese/add/', views.add_diocese, name='add_diocese'),
    path('pastorate/add/', views.add_pastorate, name='add_pastorate'),
    path('church/add/', views.add_church, name='add_church'),
]
