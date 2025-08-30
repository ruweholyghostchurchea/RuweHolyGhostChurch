from django.urls import path
from . import views

app_name = 'church_structure'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-diocese/', views.add_diocese, name='add_diocese'),
    path('add-pastorate/', views.add_pastorate, name='add_pastorate'),
    path('add-church/', views.add_church, name='add_church'),
    path('api/pastorates/<int:diocese_id>/', views.get_pastorates, name='get_pastorates'),
    path('api/churches/<int:pastorate_id>/', views.get_churches, name='get_churches'),
    # Detail views
    path('diocese/<slug:diocese_slug>/', views.diocese_detail, name='diocese_detail'),
    path('pastorate/<slug:pastorate_slug>/', views.pastorate_detail, name='pastorate_detail'),
    path('church/<slug:church_slug>/', views.church_detail, name='church_detail'),
    # Edit views
    path('diocese/<slug:diocese_slug>/edit/', views.edit_diocese, name='edit_diocese'),
    path('pastorate/<slug:pastorate_slug>/edit/', views.edit_pastorate, name='edit_pastorate'),
    path('church/<slug:church_slug>/edit/', views.edit_church, name='edit_church'),
    # Delete views
    path('diocese/<slug:diocese_slug>/delete/', views.delete_diocese, name='delete_diocese'),
    path('pastorate/<slug:pastorate_slug>/delete/', views.delete_pastorate, name='delete_pastorate'),
    path('church/<slug:church_slug>/delete/', views.delete_church, name='delete_church'),
    path('api/search-members/', views.search_members, name='search_members'),
]