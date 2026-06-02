from django.conf import settings
from django.templatetags.static import static


def _site_base_url(request):
    configured_url = getattr(settings, 'SITE_URL', '')
    if configured_url:
        return configured_url.rstrip('/')

    if request is not None:
        return request.build_absolute_uri('/').rstrip('/')

    return ''


def _absolute_url(base_url, path):
    if not base_url:
        return path

    if not path.startswith('/'):
        path = f'/{path}'

    return f'{base_url}{path}'


def seo(request):
    site_base_url = _site_base_url(request)
    current_path = request.path if request is not None else '/'

    return {
        'seo_site_name': getattr(settings, 'SITE_NAME', 'Курская федерация настольного тенниса'),
        'seo_default_description': getattr(settings, 'SITE_DESCRIPTION', ''),
        'site_base_url': site_base_url,
        'current_absolute_url': _absolute_url(site_base_url, current_path),
        'default_og_image_url': _absolute_url(site_base_url, static('images/home.jpg')),
        'site_logo_url': _absolute_url(site_base_url, static('images/base/logo.png')),
    }
