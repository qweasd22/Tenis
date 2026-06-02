from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    

