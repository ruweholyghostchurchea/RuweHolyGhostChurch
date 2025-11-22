"""
URL patterns for Visitors app
All URLs are namespaced under 'visitors:'
"""

from django.urls import path
from . import views

app_name = 'visitors'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('list/', views.visitor_list, name='visitor_list'),
    path('statistics/', views.visitor_statistics, name='visitor_statistics'),
    
    # CRUD operations
    path('add/', views.visitor_add, name='visitor_add'),
    path('<int:visitor_id>/', views.visitor_detail, name='visitor_detail'),
    path('<int:visitor_id>/edit/', views.visitor_edit, name='visitor_edit'),
    path('<int:visitor_id>/delete/', views.visitor_delete, name='visitor_delete'),
    
    # Visitor engagement
    path('<int:visitor_id>/register-visit/', views.register_visit, name='register_visit'),
    path('<int:visitor_id>/record-followup/', views.record_followup, name='record_followup'),
    path('<int:visitor_id>/convert-to-member/', views.convert_to_member, name='convert_to_member'),
]
