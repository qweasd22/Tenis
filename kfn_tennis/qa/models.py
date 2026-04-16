from django.db import models


class QaIndex(models.Model):
    SOURCE_TYPES = (
        ("news", "Новость"),
        ("project", "Проект"),
        ("team_member", "Игрок"),
        ("coach", "Тренер"),
        ("judge", "Судья"),
        ("page", "Страница"),
    )

    source_type = models.CharField(max_length=30, choices=SOURCE_TYPES, db_index=True)
    source_id = models.PositiveIntegerField(db_index=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    url = models.CharField(max_length=500, blank=True)

    # новые поля
    summary = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Индекс Q&A"
        verbose_name_plural = "Индекс Q&A"
        indexes = [
            models.Index(fields=["source_type", "is_published"]),
        ]

    def __str__(self):
        return f"{self.get_source_type_display()}: {self.title}"