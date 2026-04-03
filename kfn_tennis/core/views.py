from django.shortcuts import render
from .models import Partner
from news.models import News

def home(request):
    partners = list(Partner.objects.all())
    latest_news = News.objects.filter(published=True).order_by('-created_at')[:6]

    # Группируем партнеров по 4 для карусели
    partner_groups = [partners[i:i+4] for i in range(0, len(partners), 4)]

    context = {
        'partners': partners,
        'partner_groups': partner_groups,
        'latest_news': latest_news,
    }
    return render(request, 'core/home.html', context)