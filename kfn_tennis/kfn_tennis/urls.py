from django.contrib import admin
from django.contrib.staticfiles.views import serve as staticfiles_serve
from django.urls import path, include
from django.conf import settings
from django.views.static import serve as media_serve
from django.urls import re_path
from django.contrib.sitemaps.views import sitemap
from kfn_tennis.seo import robots_txt
from kfn_tennis.sitemaps import (
    DocumentCategorySitemap,
    MediaEventSitemap,
    NewsSitemap,
    ProjectSitemap,
    StaticPagesSitemap,
)


sitemaps = {
    'static': StaticPagesSitemap,
    'news': NewsSitemap,
    'projects': ProjectSitemap,
    'documents': DocumentCategorySitemap,
    'media': MediaEventSitemap,
}

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('core.urls')),  # подключаем core
    path('news/', include('news.urls')),
    path('structure/', include('structure.urls')),
    path('documents/', include('documents.urls')),
    path('projects/', include('projects.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('teams/', include('teams.urls')),
    path('eventcalendar/', include('eventcalendar.urls')),
    path('media/', include('MediaPhoto.urls')),
    path('qa/', include('qa.urls')),
    path('admin/', include('dashboard.urls', namespace='dashboard')),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG or settings.SERVE_STATIC_FILES:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', staticfiles_serve, {'insecure': True}),
        re_path(r'^media/(?P<path>.*)$', media_serve, {'document_root': settings.MEDIA_ROOT}),
    ]
    

