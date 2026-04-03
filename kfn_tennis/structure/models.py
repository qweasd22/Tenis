from django.db import models

class Person(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    role = models.CharField(max_length=150, blank=True, verbose_name='Должность')
    photo = models.ImageField(upload_to='persons_photos/', blank=True, null=True, verbose_name='Фото')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    # Тип для вкладок
    group = models.CharField(
        max_length=50,
        choices=[('board', 'Попечительский совет'), ('members', 'Члены федерации'),('other', 'Другое')],
        default='members',
        verbose_name='Группа'
    )

    class Meta:
        
        verbose_name = "Член федерации"
        verbose_name_plural = "Члены федерации"

    def __str__(self):
        return self.full_name