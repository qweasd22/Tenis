from django.core.paginator import Paginator
from django.shortcuts import render
from .models import TeamMember, Coach, Judge, Season

def teams_view(request):
    tab = request.GET.get('tab', 'teams')
    selected_season = request.GET.get('season', '')
    selected_gender = request.GET.get('gender', '')
    search_query = request.GET.get('search', '')

    # --- Сборные ---
    members_qs = TeamMember.objects.all()
    if selected_season:
        members_qs = members_qs.filter(season_id=selected_season)
    if selected_gender in {TeamMember.MALE, TeamMember.FEMALE}:
        members_qs = members_qs.filter(gender=selected_gender)
    if search_query:
        members_qs = members_qs.filter(full_name__icontains=search_query)
    members_paginator = Paginator(members_qs, 12)
    teams_page = members_paginator.get_page(request.GET.get('teams_page', 1))

    # --- Тренера ---
    coaches_qs = Coach.objects.all()
    coaches_paginator = Paginator(coaches_qs, 12)
    coaches_page = coaches_paginator.get_page(request.GET.get('coaches_page', 1))

    # --- Судьи ---
    judges_qs = Judge.objects.all()
    judges_paginator = Paginator(judges_qs, 12)
    judges_page = judges_paginator.get_page(request.GET.get('judges_page', 1))

    seasons = Season.objects.all().order_by('-year')

    return render(request, 'teams/teams.html', {
        'active_tab': tab,
        'selected_season': selected_season,
        'selected_gender': selected_gender,
        'search_query': search_query,
        'seasons': seasons,
        'teams_page': teams_page,
        'coaches_page': coaches_page,
        'judges_page': judges_page,
    })
