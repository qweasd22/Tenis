from django.db import models

class Season(models.Model):
    year = models.PositiveIntegerField(unique=True, verbose_name='Год')
    team_list_pdf = models.FileField("Список игроков PDF", upload_to='team_lists/', blank=True, null=True)
    def __str__(self):
        return str(self.year)
    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'


class Player(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    birth_date = models.DateField(verbose_name='Дата рождения')
    rank = models.CharField(max_length=50, blank=True, verbose_name='Разряд')
    organization = models.CharField(max_length=100, blank=True, verbose_name='Организация')
    photo = models.ImageField(upload_to='players/', blank=True, null=True, verbose_name='Фото')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='players', verbose_name='Сезон')
    

    def __str__(self):
        return self.full_name
