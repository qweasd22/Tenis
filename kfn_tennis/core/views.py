from django.shortcuts import render
from .models import Partner
from news.models import News

def home(request):
    partners = list(Partner.objects.all())

    # Новости для слайдера — только отмеченные галочкой
    priority_news = list(News.objects.filter(published=True, show_in_slider=True).order_by('-created_at'))
    slider_news = priority_news[:6]

    # Последние новости для списка под слайдером, исключаем уже показанные в слайдере
    latest_news = list(News.objects.filter(published=True).exclude(id__in=[n.id for n in priority_news]).order_by('-created_at'))
    latest_news_display = latest_news[:6]

    # Группируем партнеров по 4 для карусели
    partner_groups = [partners[i:i+4] for i in range(0, len(partners), 4)]

    context = {
        'partners': partners,
        'partner_groups': partner_groups,
        'latest_news': latest_news_display,
        'slider_news': slider_news
    }
    return render(request, 'core/home.html', context)