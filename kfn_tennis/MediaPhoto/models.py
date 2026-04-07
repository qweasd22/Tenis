from django.db import models
from django.urls import reverse

class MediaEvent(models.Model):
    title = models.CharField("Название мероприятия", max_length=255)
    description = models.TextField("Описание", blank=True)
    date = models.DateField("Дата")
    cover = models.ImageField("Обложка", upload_to='media/covers/', blank=True, null=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Мероприятие"
        verbose_name_plural = "Медиа"

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('media:media_detail', args=[self.pk])

class MediaPhoto(models.Model):
    event = models.ForeignKey(MediaEvent, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField("Фото", upload_to='media/photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event.title}"