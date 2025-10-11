"""
Public Website URL Configuration for ruweholyghostchurch.org
Public-facing website (no authentication required)
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import public website views (to be created)
# from public_site import views

urlpatterns = [
    # Public website URLs will be added here
    # path('', views.home, name='public_home'),
    # path('about/', views.about, name='public_about'),
    # path('contact/', views.contact, name='public_contact'),
    # path('events/', views.events, name='public_events'),
    # path('sermons/', views.sermons, name='public_sermons'),
    
    # Placeholder for now
    path('', lambda request: __import__('django.http').HttpResponse('Welcome to Ruwe Holy Ghost Church - Public Website (Coming Soon)')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
