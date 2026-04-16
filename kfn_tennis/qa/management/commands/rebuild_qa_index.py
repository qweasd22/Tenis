import re

from django.core.management.base import BaseCommand
from django.utils.html import strip_tags

from qa.models import QaIndex
from news.models import News
from projects.models import Project
from teams.models import TeamMember, Coach, Judge


def clean_text(value):
    if not value:
        return ""
    text = strip_tags(str(value))
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def short_text(text, limit=300):
    text = clean_text(text)
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."


class Command(BaseCommand):
    help = "Пересобирает индекс Q&A"

    def handle(self, *args, **kwargs):
        QaIndex.objects.all().delete()

        for item in News.objects.filter(published=True):
            full_text = clean_text(item.full_description)
            keywords = f"{item.title} новость новости федерация теннис"
            QaIndex.objects.create(
                source_type="news",
                source_id=item.id,
                title=clean_text(item.title),
                content=full_text,
                summary=short_text(full_text),
                keywords=clean_text(keywords),
                url=item.get_absolute_url(),
                published_at=item.created_at,
                is_published=item.published,
            )

        for item in Project.objects.filter(is_active=True):
            full_text = " ".join(filter(None, [
                clean_text(item.short_description),
                clean_text(item.full_description),
                clean_text(item.location),
                clean_text(item.contacts),
                clean_text(item.get_status_display()),
                clean_text(item.category.title if item.category_id else ""),
            ]))
            keywords = f"{item.title} проект проекты {item.get_status_display()}"
            QaIndex.objects.create(
                source_type="project",
                source_id=item.id,
                title=clean_text(item.title),
                content=full_text,
                summary=short_text(item.short_description or full_text),
                keywords=clean_text(keywords),
                url=item.get_absolute_url(),
                is_published=item.is_active,
            )

        for item in TeamMember.objects.select_related("season").all():
            full_text = " ".join(filter(None, [
                clean_text(item.full_name),
                clean_text(item.rank),
                clean_text(item.coach),
                clean_text(item.get_gender_display() if item.gender else ""),
                clean_text(str(item.rating) if item.rating is not None else ""),
                clean_text(f"сезон {item.season.year}" if item.season_id else ""),
                "игрок сборная команда теннис"
            ]))
            QaIndex.objects.create(
                source_type="team_member",
                source_id=item.id,
                title=clean_text(item.full_name),
                content=full_text,
                summary=short_text(full_text, 180),
                keywords="игрок сборная теннис команда рейтинг тренер",
                url="/teams/",
                is_published=True,
            )

        for item in Coach.objects.all():
            full_text = " ".join(filter(None, [
                clean_text(item.full_name),
                clean_text(item.category),
                "тренер теннис команда"
            ]))
            QaIndex.objects.create(
                source_type="coach",
                source_id=item.id,
                title=clean_text(item.full_name),
                content=full_text,
                summary=short_text(full_text, 180),
                keywords="тренер тренеры теннис категория",
                url="/teams/",
                is_published=True,
            )

        for item in Judge.objects.all():
            full_text = " ".join(filter(None, [
                clean_text(item.full_name),
                clean_text(item.category),
                "судья судьи теннис"
            ]))
            QaIndex.objects.create(
                source_type="judge",
                source_id=item.id,
                title=clean_text(item.full_name),
                content=full_text,
                summary=short_text(full_text, 180),
                keywords="судья судьи теннис категория",
                url="/teams/",
                is_published=True,
            )

        self.stdout.write(self.style.SUCCESS("Индекс Q&A пересобран"))