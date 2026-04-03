from django.contrib import admin
from .models import Person

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'group', 'is_active', )
    list_filter = ('group', 'is_active')
    search_fields = ('full_name', 'role',)
    readonly_fields = ('photo_preview',)
    
    fieldsets = (
        (None, {
            'fields': ('full_name', 'role', 'group', 'is_active')
        }),
        ('Фото и биография', {
            'fields': ('photo', 'photo_preview', )
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return f'<img src="{obj.photo.url}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 50%;" />'
        return "-"
    photo_preview.allow_tags = True
    photo_preview.short_description = "Превью фото"