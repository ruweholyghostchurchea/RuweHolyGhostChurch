
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class SubdomainMiddleware(MiddlewareMixin):
    """
    Middleware to detect subdomain and route requests accordingly
    
    Subdomains:
    - cms.ruweholyghostchurch.org -> Admin CMS
    - members.ruweholyghostchurch.org -> Members Portal
    - ruweholyghostchurch.org (or www) -> Public Website
    """
    
    def process_request(self, request):
        # Get the full host
        host = request.get_host().lower()
        
        # For development (localhost, Replit domains)
        if 'localhost' in host or 'replit' in host or '127.0.0.1' in host:
            # Default to CMS (admin dashboard) for development
            request.subdomain = 'cms'
            request.urlconf = 'ruweholyghostchurch.cms_urls'
            return
        
        # Extract subdomain from host
        parts = host.split('.')
        
        # Handle different subdomain cases
        if len(parts) >= 3:
            # Has subdomain
            subdomain = parts[0]
            
            if subdomain == 'cms':
                request.subdomain = 'cms'
                request.urlconf = 'ruweholyghostchurch.cms_urls'
            elif subdomain == 'members':
                request.subdomain = 'members'
                request.urlconf = 'ruweholyghostchurch.members_urls'
            elif subdomain == 'www':
                # www is treated as public site
                request.subdomain = 'public'
                request.urlconf = 'ruweholyghostchurch.public_urls'
            else:
                # Unknown subdomain, default to public
                request.subdomain = 'public'
                request.urlconf = 'ruweholyghostchurch.public_urls'
        else:
            # No subdomain (root domain) - public site
            request.subdomain = 'public'
            request.urlconf = 'ruweholyghostchurch.public_urls'
