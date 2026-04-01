from django.db import models
from django.core.exceptions import ValidationError


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название события")

    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")

    start_time = models.TimeField(null=True, blank=True, verbose_name="Время начала")
    end_time = models.TimeField(null=True, blank=True, verbose_name="Время окончания")

    pdf = models.FileField(upload_to='events_pdfs/', null=True, blank=True, verbose_name="PDF файл")

    is_current = models.BooleanField(default=True, verbose_name="Актуальное")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def clean(self):
        # Если дата окончания не указана — делаем её равной дате начала
        if not self.end_date:
            self.end_date = self.start_date

        # Проверка диапазона дат
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("Дата окончания не может быть раньше даты начала.")

        # Проверка времени
        if self.start_time and self.end_time:
            if self.end_time < self.start_time and self.start_date == self.end_date:
                raise ValidationError("Время окончания не может быть раньше времени начала.")

    def date_range(self):
        if self.start_date == self.end_date:
            return self.start_date.strftime("%d.%m.%Y")
        return f"{self.start_date.strftime('%d.%m.%Y')} - {self.end_date.strftime('%d.%m.%Y')}"

    date_range.short_description = "Даты"

    def __str__(self):
        return self.title
