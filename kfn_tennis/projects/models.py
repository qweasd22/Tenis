from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from .validators import validate_project_file


class ProjectCategory(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name='Slug'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )

    class Meta:
        verbose_name = 'Категория проектов'
        verbose_name_plural = 'Категории проектов'
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while ProjectCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProjectStatus(models.TextChoices):
    ACTIVE = 'active', 'Активный'
    PLANNED = 'planned', 'Планируется'
    ARCHIVE = 'archive', 'Архивный'


class Project(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название проекта'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name='Slug'
    )

    category = models.ForeignKey(
        ProjectCategory,
        on_delete=models.PROTECT,
        related_name='projects',
        verbose_name='Категория'
    )

    short_description = models.TextField(
        verbose_name='Краткое описание'
    )

    full_description = CKEditor5Field(
    verbose_name='Полное описание',
    config_name='default'
)

    main_image = models.ImageField(
        upload_to='projects/main/',
        verbose_name='Главное изображение'
    )

    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.ACTIVE,
        verbose_name='Статус проекта'
    )

    start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата начала'
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата окончания'
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Место проведения'
    )

    prize_fund = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Призовой фонд'
    )

    contacts = models.TextField(
        blank=True,
        verbose_name='Контактная информация'
    )

    attachment = models.FileField(
        upload_to='projects/docs/',
        blank=True,
        null=True,
        validators=[validate_project_file],
        verbose_name='Положение / регламент'
    )

    external_link = models.URLField(
        blank=True,
        verbose_name='Ссылка на результаты'
    )

    gallery_link = models.URLField(
        blank=True,
        verbose_name='Ссылка на фотогалерею'
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Показывать на сайте'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['order', '-start_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
