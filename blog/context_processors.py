from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

def global_settings(request):
    return {
        'SITE_DOMAIN': settings.SITE_DOMAIN,
        'SITE_SUBDOMAIN': get_current_site(request).domain,
        'SITE_NAME': get_current_site(request).name,
        'SITE_TITLE': settings.SITE_TITLE,
        'SITE_YEAR': settings.SITE_YEAR,
        'GITHUB_URL': settings.GITHUB_URL,
        'PORTFOLIO_URL': settings.PORTFOLIO_URL,
    }
