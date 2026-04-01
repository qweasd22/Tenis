from django.contrib import admin
from django.utils.html import format_html
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "date_range",
        "start_time",
        "is_current",
        "pdf_link",
    )

    list_filter = (
        "is_current",
        "start_date",
    )

    search_fields = ("title",)

    ordering = ("-start_date",)

    readonly_fields = ("created_at",)

    fieldsets = (
        ("Основная информация", {
            "fields": ("title", "is_current")
        }),
        ("Даты", {
            "fields": ("start_date", "end_date")
        }),
        ("Время", {
            "fields": ("start_time", "end_time")
        }),
        ("Документы", {
            "fields": ("pdf",)
        }),
        ("Системная информация", {
            "fields": ("created_at",),
        }),
    )

    def pdf_link(self, obj):
        if obj.pdf:
            return format_html(
                '<a href="{}" target="_blank">📄 Скачать</a>',
                obj.pdf.url
            )
        return "-"

    pdf_link.short_description = "PDF"
