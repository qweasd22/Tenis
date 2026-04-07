from django.contrib import admin
from .models import MediaEvent, MediaPhoto


class MediaPhotoInline(admin.TabularInline):
    model = MediaPhoto
    extra = 1


@admin.register(MediaEvent)
class MediaEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    inlines = [MediaPhotoInline]


@admin.register(MediaPhoto)
class MediaPhotoAdmin(admin.ModelAdmin):
    list_display = ('event', 'uploaded_at')