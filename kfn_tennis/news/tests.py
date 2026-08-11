from django.test import TestCase
from django.urls import reverse

from news.models import News


class NewsModelTests(TestCase):
    def test_save_generates_safe_slug_for_blank_title(self):
        news = News(title="   ", published=True)
        news.save()

        self.assertTrue(news.slug)
        self.assertEqual(news.get_absolute_url(), reverse("news:news_detail", kwargs={"slug": news.slug}))
