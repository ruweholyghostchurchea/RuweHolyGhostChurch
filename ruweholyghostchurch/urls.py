"""
URL configuration for ruweholyghostchurch project.

This is the fallback URL configuration used when no subdomain routing is applied.
The SubdomainMiddleware will override this with:
- cms_urls.py for cms.ruweholyghostchurch.org (Admin CMS)
- members_urls.py for members.ruweholyghostchurch.org (Members Portal)
- public_urls.py for ruweholyghostchurch.org (Public Website)

In development, defaults to CMS URLs.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

def redirect_to_dashboard(request):
    return redirect('dashboard:index')

# Default to CMS URLs (for development and fallback)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_dashboard, name='home'),
    path('auth/', include('authentication.urls', namespace='authentication')),
    path('dashboard/', include('dashboard.urls')),
    path('church-structure/', include('church_structure.urls', namespace='church_structure')),
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