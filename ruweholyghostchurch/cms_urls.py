"""
CMS URL Configuration for cms.ruweholyghostchurch.org
Admin-only Church Management System
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redirect_to_dashboard(request):
    return redirect('dashboard:index')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_dashboard, name='home'),
    path('auth/', include('authentication.urls', namespace='authentication')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('church-structure/', include('church_structure.urls', namespace='church_structure')),
    path('ruwe-administration/', include('ruwe_administration.urls', namespace='ruwe_administration')),
    path('members/', include('members.urls', namespace='members')),
    path('visitors/', include('visitors.urls', namespace='visitors')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('finance/', include('finance.urls', namespace='finance')),
    path('bulk-sms/', include('bulk_sms.urls', namespace='bulk_sms')),
    path('equipment/', include('equipment.urls', namespace='equipment')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('church-settings/', include('church_settings.urls', namespace='church_settings')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
