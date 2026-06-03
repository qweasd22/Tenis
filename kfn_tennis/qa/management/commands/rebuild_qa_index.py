from django.core.management.base import BaseCommand

from qa.indexers import rebuild_all


class Command(BaseCommand):
    help = "Пересобирает индекс Q&A"

    def handle(self, *args, **kwargs):
        indexed_count = rebuild_all()
        self.stdout.write(self.style.SUCCESS(f"Индекс Q&A пересобран. Записей: {indexed_count}"))
