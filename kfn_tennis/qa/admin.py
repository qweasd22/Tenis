from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path

from qa.indexers import rebuild_all
from qa.models import QaIndex


@admin.register(QaIndex)
class QaIndexAdmin(admin.ModelAdmin):
    change_list_template = "admin/qa/qaindex/change_list.html"
    list_display = ("title", "source_type", "is_published", "published_at", "url")
    list_filter = ("source_type", "is_published")
    search_fields = ("title", "summary", "keywords", "content")
    readonly_fields = ("created_at",)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "rebuild/",
                self.admin_site.admin_view(self.rebuild_index),
                name="qa_qaindex_rebuild",
            ),
        ]
        return custom_urls + urls

    def rebuild_index(self, request):
        if request.method != "POST":
            return redirect("admin:qa_qaindex_changelist")

        indexed_count = rebuild_all()
        messages.success(request, f"Индекс Q&A пересобран. Записей: {indexed_count}.")
        return redirect("admin:qa_qaindex_changelist")
