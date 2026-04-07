from django.contrib import admin
from .models import Season, TeamMember, Coach, Judge

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('year', 'team_list_pdf')
    search_fields = ('year',)
    ordering = ('-year',)

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'rank', 'coach', 'rating', 'season')
    list_filter = ('season', 'rank')
    search_fields = ('full_name', 'coach')
    ordering = ('full_name',)

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'category')
    search_fields = ('full_name', 'category')
    ordering = ('full_name',)

@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'category')
    search_fields = ('full_name', 'category')
    ordering = ('full_name',)