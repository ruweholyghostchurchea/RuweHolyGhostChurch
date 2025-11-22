"""
URL patterns for Attendance app
All URLs are namespaced under 'attendance:'
"""

from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('sessions/', views.session_list, name='session_list'),
    path('statistics/', views.attendance_statistics, name='attendance_statistics'),
    path('absence-tracking/', views.absence_tracking, name='absence_tracking'),
    
    # Session CRUD operations
    path('session/create/', views.session_create, name='session_create'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('session/<int:session_id>/edit/', views.session_edit, name='session_edit'),
    path('session/<int:session_id>/delete/', views.session_delete, name='session_delete'),
    
    # Attendance marking
    path('session/<int:session_id>/mark/', views.mark_attendance, name='mark_attendance'),
    path('record/<int:record_id>/edit/', views.edit_attendance_record, name='edit_attendance_record'),
    
    # Session management
    path('session/<int:session_id>/lock/', views.lock_session, name='lock_session'),
    path('session/<int:session_id>/unlock/', views.unlock_session, name='unlock_session'),
]
