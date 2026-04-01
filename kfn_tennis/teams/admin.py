from django.contrib import admin
from .models import Season, Player

# Inline для игроков внутри сезона (опционально)
class PlayerInline(admin.TabularInline):
    model = Player
    extra = 0
    fields = ('full_name', 'birth_date', 'rank', 'organization', 'photo')
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.photo:
            return f'<img src="{obj.photo.url}" width="60" style="border-radius:5px;" />'
        return "-"
    photo_preview.allow_tags = True
    photo_preview.short_description = "Фото"

# Админка для сезона
@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('year', 'team_list_pdf')
    search_fields = ('year',)
    ordering = ('-year',)
    inlines = [PlayerInline]

# Админка для игрока
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'season', 'birth_date', 'rank', 'organization', 'photo_preview')
    list_filter = ('season',)
    search_fields = ('full_name', 'organization', 'rank')
    readonly_fields = ('photo_preview',)
    ordering = ('full_name',)

    def photo_preview(self, obj):
        if obj.photo:
            return f'<img src="{obj.photo.url}" width="60" style="border-radius:5px;" />'
        return "-"
    photo_preview.allow_tags = True
    photo_preview.short_description = "Фото"
