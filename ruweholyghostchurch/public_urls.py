"""
Public Website URL Configuration for ruweholyghostchurch.org
Public-facing website (no authentication required)
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Public website URLs
    path('', include('public_site.urls')),
    # Authentication URLs for login/logout
    path('auth/', include('authentication.urls', namespace='authentication')),
    # Members Portal (for development - in production this would be members.domain)
    path('members/', include('members_portal.urls')),
    # Admin Dashboard (for staff users - in production this would be cms.domain)
    path('dashboard/', include('dashboard.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
