from django.conf import settings

def global_settings(request):
    return {
        'SITE_URL': settings.SITE_URL,
        'SITE_NAME': settings.SITE_NAME,
        'SITE_TITLE': settings.SITE_TITLE,
        'SITE_YEAR': settings.SITE_YEAR,
        'GITHUB_URL': settings.GITHUB_URL,
        'PORTFOLIO_URL': settings.PORTFOLIO_URL,
    }
