from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from documents.models import Category
from MediaPhoto.models import MediaEvent
from news.models import News
from projects.models import Project


class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return News.objects.filter(published=True).order_by('-created_at')

    def lastmod(self, item):
        return item.created_at

    def location(self, item):
        return item.get_absolute_url()


class ProjectSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Project.objects.filter(
            is_active=True,
            category__is_active=True,
        ).select_related('category').order_by('order', '-start_date')

    def lastmod(self, item):
        return item.updated_at

    def location(self, item):
        return item.get_absolute_url()


class DocumentCategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Category.objects.all().order_by('order', 'name')

    def location(self, item):
        return reverse('documents:category', kwargs={'slug': item.slug})


class MediaEventSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return MediaEvent.objects.all().order_by('-date')

    def lastmod(self, item):
        return item.date

    def location(self, item):
        return item.get_absolute_url()


class StaticPagesSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9

    def items(self):
        return (
            'core:home',
            'news:news_list',
            'structure:structure_home',
            'documents:categories',
            'projects:list',
            'teams:teams',
            'calendar:calendar',
            'media:media_list',
        )

    def location(self, item):
        return reverse(item)
