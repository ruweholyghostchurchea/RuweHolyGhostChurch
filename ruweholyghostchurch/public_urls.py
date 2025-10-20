"""
Public Website URL Configuration for ruweholyghostchurch.org
Public-facing website (no authentication required)
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    # Public website URLs
    path('', include('public_site.urls')),
    # Authentication URLs for login/logout
    path('auth/', include('authentication.urls', namespace='authentication')),
    # Members Portal (for development - in production this would be members.domain)
    path('members/', include('members_portal.urls')),
    # Admin Dashboard (for staff users - in production this would be cms.domain)
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    # Include all CMS URLs for development access
    path('church-structure/', include('church_structure.urls', namespace='church_structure')),
    path('ruwe-administration/', include('ruwe_administration.urls', namespace='ruwe_administration')),
    path('members-admin/', include('members.urls', namespace='members')),
    path('visitors/', include('visitors.urls', namespace='visitors')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('finance/', include('finance.urls', namespace='finance')),
    path('email-system/', include('email_system.urls', namespace='email_system')),
    path('bulk-sms/', include('bulk_sms.urls', namespace='bulk_sms')),
    path('equipment/', include('equipment.urls', namespace='equipment')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('church-settings/', include('church_settings.urls', namespace='church_settings')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
