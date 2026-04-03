from django.db import models
from django.utils import timezone
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
class News(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(unique=True)
    full_description = CKEditor5Field(
    verbose_name='Полное описание',
    config_name='default'
)
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='Изображение')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    published = models.BooleanField(default=True, verbose_name='Опубликовано')
    show_in_slider = models.BooleanField(
    default=False,
    verbose_name='Показать в слайдере',
    help_text='Отметьте, если эта новость должна отображаться в слайдере на главной'
)
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'slug': self.slug})
