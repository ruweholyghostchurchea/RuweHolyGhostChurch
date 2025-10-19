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
    path('dashboard/', include('dashboard.urls')),
    path('church-structure/', include('church_structure.urls')),
    path('ruwe-administration/', include('ruwe_administration.urls')),
    path('members/', include('members.urls')),
    path('visitors/', include('visitors.urls')),
    path('attendance/', include('attendance.urls')),
    path('finance/', include('finance.urls')),
    path('bulk-sms/', include('bulk_sms.urls')),
    path('equipment/', include('equipment.urls')),
    path('reports/', include('reports.urls')),
    path('church-settings/', include('church_settings.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
