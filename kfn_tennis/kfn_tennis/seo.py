from django.conf import settings
from django.http import HttpResponse


def robots_txt(request):
    site_url = getattr(settings, 'SITE_URL', '').rstrip('/')
    if not site_url:
        site_url = request.build_absolute_uri('/').rstrip('/')

    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        'Disallow: /django-admin/',
        'Disallow: /ckeditor5/',
        'Disallow: /qa/ask/',
        '',
        f'Sitemap: {site_url}/sitemap.xml',
    ]

    return HttpResponse('\n'.join(lines), content_type='text/plain; charset=utf-8')
