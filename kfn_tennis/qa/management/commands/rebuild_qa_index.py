import re
from datetime import datetime, time

from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

from qa.models import QaIndex
from core.models import Partner
from documents.models import Category, Document
from eventcalendar.models import Event
from MediaPhoto.models import MediaEvent
from news.models import News
from projects.models import Project
from structure.models import Person
from teams.models import TeamMember, Coach, Judge, Season


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


def join_text(*parts):
    return " ".join(filter(None, (clean_text(part) for part in parts)))


def format_date(value):
    if not value:
        return ""
    return value.strftime("%d.%m.%Y")


def date_to_datetime(value):
    if not value:
        return None
    dt = datetime.combine(value, time.min)
    return timezone.make_aware(dt) if timezone.is_naive(dt) else dt


def format_date_range(start_date, end_date):
    if not start_date:
        return ""
    actual_end_date = end_date or start_date
    if start_date == actual_end_date:
        return format_date(start_date)
    return f"{format_date(start_date)} - {format_date(actual_end_date)}"


def file_url(file_field):
    if not file_field:
        return ""
    try:
        return file_field.url
    except ValueError:
        return ""


STATIC_PAGES = (
    {
        "title": "Главная",
        "url_name": "core:home",
        "content": (
            "Главная страница Курской федерации настольного тенниса. "
            "Новости, слайдер, партнеры, основные разделы сайта и быстрый переход к материалам федерации."
        ),
        "keywords": "главная сайт федерация настольный теннис курск новости партнеры",
    },
    {
        "title": "О Федерации",
        "url_name": "structure:structure_home",
        "content": (
            "Структура федерации, попечительский совет, члены федерации, руководство и активные участники."
        ),
        "keywords": "федерация структура попечительский совет члены руководство",
    },
    {
        "title": "Новости",
        "url_name": "news:news_list",
        "content": "Все опубликованные новости Курской федерации настольного тенниса.",
        "keywords": "новости публикации объявления федерация",
    },
    {
        "title": "Документы",
        "url_name": "documents:categories",
        "content": "Официальные документы, положения, регламенты, категории документов и файлы для скачивания.",
        "keywords": "документы положения регламенты файлы скачать",
    },
    {
        "title": "Сборные",
        "url_name": "teams:teams",
        "content": "Сборные команды, игроки, тренеры, судьи, сезоны, рейтинги и списки игроков.",
        "keywords": "сборные команда игроки тренеры судьи сезон рейтинг",
    },
    {
        "title": "Календарь",
        "url_name": "calendar:calendar",
        "content": "Календарь соревнований, турниров и событий федерации с датами, временем и PDF-файлами.",
        "keywords": "календарь расписание события турниры соревнования даты",
    },
    {
        "title": "Проекты",
        "url_name": "projects:list",
        "content": "Проекты федерации, программы, статусы, места проведения, контакты и регламенты.",
        "keywords": "проекты программы мероприятия статус контакты",
    },
    {
        "title": "Медиа",
        "url_name": "media:media_list",
        "content": "Медиа, фотогалереи, фотографии соревнований, проектов и мероприятий.",
        "keywords": "медиа фото фотографии галерея альбом события",
    },
)


class Command(BaseCommand):
    help = "Пересобирает индекс Q&A"

    def handle(self, *args, **kwargs):
        QaIndex.objects.all().delete()

        for index, page in enumerate(STATIC_PAGES, start=1):
            QaIndex.objects.create(
                source_type="page",
                source_id=index,
                title=page["title"],
                content=clean_text(page["content"]),
                summary=short_text(page["content"]),
                keywords=clean_text(page["keywords"]),
                url=reverse(page["url_name"]),
                is_published=True,
            )

        for item in News.objects.filter(published=True):
            full_text = clean_text(item.full_description)
            keywords = f"{item.title} новость новости федерация теннис настольный теннис Курск"
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

        for item in Project.objects.filter(is_active=True, category__is_active=True).select_related("category"):
            full_text = join_text(
                item.short_description,
                item.full_description,
                item.location,
                item.contacts,
                item.prize_fund,
                item.get_status_display(),
                item.category.title if item.category_id else "",
                format_date(item.start_date),
                format_date(item.end_date),
                item.external_link,
                item.gallery_link,
            )
            keywords = f"{item.title} проект проекты программа {item.get_status_display()} {item.category.title}"
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

        for category in Category.objects.all():
            full_text = join_text(
                category.name,
                "раздел документов категория документы положения регламенты файлы",
            )
            QaIndex.objects.create(
                source_type="document_category",
                source_id=category.id,
                title=clean_text(category.name),
                content=full_text,
                summary=short_text(full_text, 180),
                keywords=clean_text(f"{category.name} документы категория положения регламенты"),
                url=reverse("documents:category", kwargs={"slug": category.slug}),
                is_published=True,
            )

        for item in Document.objects.select_related("category").prefetch_related("tags").all():
            tags = " ".join(item.tags.names())
            full_text = join_text(
                item.title,
                item.description,
                item.category.name if item.category_id else "",
                tags,
                format_date(item.created_at),
                "документ файл скачать положение регламент материалы федерации",
            )
            QaIndex.objects.create(
                source_type="document",
                source_id=item.id,
                title=clean_text(item.title),
                content=full_text,
                summary=short_text(item.description or full_text, 220),
                keywords=clean_text(f"{item.title} {tags} документ документы положение регламент файл скачать"),
                url=file_url(item.file) or reverse("documents:category", kwargs={"slug": item.category.slug}),
                published_at=item.created_at,
                is_published=True,
            )

        for item in Event.objects.all():
            date_range = format_date_range(item.start_date, item.end_date)
            time_range = " ".join(filter(None, [
                item.start_time.strftime("%H:%M") if item.start_time else "",
                item.end_time.strftime("%H:%M") if item.end_time else "",
            ]))
            full_text = join_text(
                item.title,
                date_range,
                time_range,
                "календарь событие турнир соревнование расписание PDF",
            )
            QaIndex.objects.create(
                source_type="event",
                source_id=item.id,
                title=clean_text(item.title),
                content=full_text,
                summary=short_text(full_text, 220),
                keywords=clean_text(f"{item.title} календарь событие события турнир соревнование расписание"),
                url=item.pdf_url() or reverse("calendar:calendar"),
                published_at=date_to_datetime(item.start_date),
                is_published=item.is_current,
            )

        for item in MediaEvent.objects.all():
            full_text = join_text(
                item.title,
                item.description,
                format_date(item.date),
                "медиа фото фотографии фотогалерея галерея альбом соревнования мероприятия",
            )
            QaIndex.objects.create(
                source_type="media",
                source_id=item.id,
                title=clean_text(item.title),
                content=full_text,
                summary=short_text(item.description or full_text, 220),
                keywords=clean_text(f"{item.title} медиа фото фотографии галерея альбом"),
                url=item.get_absolute_url(),
                published_at=date_to_datetime(item.date),
                is_published=True,
            )

        for item in Person.objects.filter(is_active=True):
            group = item.get_group_display() if item.group else ""
            full_text = join_text(
                item.full_name,
                item.role,
                group,
                "федерация структура попечительский совет члены федерации руководство",
            )
            QaIndex.objects.create(
                source_type="person",
                source_id=item.id,
                title=clean_text(item.full_name),
                content=full_text,
                summary=short_text(full_text, 180),
                keywords=clean_text(f"{item.full_name} {item.role} {group} федерация структура совет"),
                url=reverse("structure:structure_home"),
                is_published=True,
            )

        for item in Partner.objects.all():
            full_text = join_text(
                item.name,
                item.url,
                "партнер партнеры спонсор федерации настольного тенниса",
            )
            QaIndex.objects.create(
                source_type="partner",
                source_id=item.id,
                title=clean_text(item.name),
                content=full_text,
                summary=short_text(full_text, 180),
                keywords=clean_text(f"{item.name} партнер партнеры спонсор"),
                url=item.url or reverse("core:home"),
                is_published=True,
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
                keywords="игрок сборная теннис команда рейтинг тренер спортсмен",
                url=reverse("teams:teams"),
                is_published=True,
            )

        for item in Season.objects.all():
            full_text = join_text(
                f"Сезон {item.year}",
                "сборная команда игроки список игроков PDF сезон",
            )
            QaIndex.objects.create(
                source_type="season",
                source_id=item.id,
                title=f"Сезон {item.year}",
                content=full_text,
                summary=short_text(full_text, 180),
                keywords=clean_text(f"сезон {item.year} сборная команда список игроков"),
                url=file_url(item.team_list_pdf) or reverse("teams:teams"),
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
                url=reverse("teams:teams"),
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
                url=reverse("teams:teams"),
                is_published=True,
            )

        self.stdout.write(self.style.SUCCESS("Индекс Q&A пересобран"))
