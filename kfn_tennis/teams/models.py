from django.db import models

class Season(models.Model):
    year = models.PositiveIntegerField(unique=True, verbose_name='Год')
    team_list_pdf = models.FileField("Список игроков PDF", upload_to='team_lists/', blank=True, null=True)

    def __str__(self):
        return str(self.year)

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'


class TeamMember(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    GENDER_CHOICES = [
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    ]

    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, verbose_name='Пол')
    rank = models.CharField(max_length=50, blank=True, verbose_name='Разряд')
    coach = models.CharField(max_length=100, blank=True, verbose_name='Тренер')
    rating = models.IntegerField(blank=True, null=True, verbose_name='Рейтинг')
    photo = models.ImageField(upload_to='players/', blank=True, null=True, verbose_name='Фото')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='team_members', verbose_name='Сезон')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Сборный игрок'
        verbose_name_plural = 'Сборные'


class Coach(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    category = models.CharField(max_length=50, verbose_name='Категория')
    photo = models.ImageField(upload_to='coaches/', blank=True, null=True, verbose_name='Фото')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренера'


class Judge(models.Model):
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    category = models.CharField(max_length=50, verbose_name='Категория')
    photo = models.ImageField(upload_to='judges/', blank=True, null=True, verbose_name='Фото')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Судья'
        verbose_name_plural = 'Судьи'
