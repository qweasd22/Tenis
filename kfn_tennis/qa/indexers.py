import re
from datetime import datetime, time
from html import unescape

from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

from qa.models import QaIndex


def clean_text(value):
    if not value:
        return ""
    text = strip_tags(str(value))
    text = unescape(text)
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
        "source_id": 1,
        "title": "Главная",
        "url_name": "core:home",
        "content": (
            "Главная страница Курской федерации настольного тенниса. "
            "Новости, слайдер, партнеры, основные разделы сайта и быстрый переход к материалам федерации."
        ),
        "keywords": "главная сайт федерация настольный теннис курск новости партнеры",
    },
    {
        "source_id": 2,
        "title": "О Федерации",
        "url_name": "structure:structure_home",
        "content": (
            "Структура федерации, попечительский совет, члены федерации, руководство и активные участники."
        ),
        "keywords": "федерация структура попечительский совет члены руководство",
    },
    {
        "source_id": 3,
        "title": "Новости",
        "url_name": "news:news_list",
        "content": "Все опубликованные новости Курской федерации настольного тенниса.",
        "keywords": "новости публикации объявления федерация",
    },
    {
        "source_id": 4,
        "title": "Документы",
        "url_name": "documents:categories",
        "content": "Официальные документы, положения, регламенты, категории документов и файлы для скачивания.",
        "keywords": "документы положения регламенты файлы скачать",
    },
    {
        "source_id": 5,
        "title": "Сборные",
        "url_name": "teams:teams",
        "content": "Сборные команды, игроки, тренеры, судьи, сезоны, рейтинги и списки игроков.",
        "keywords": "сборные команда игроки тренеры судьи сезон рейтинг",
    },
    {
        "source_id": 6,
        "title": "Календарь",
        "url_name": "calendar:calendar",
        "content": "Календарь соревнований, турниров и событий федерации с датами, временем и PDF-файлами.",
        "keywords": "календарь расписание события турниры соревнования даты",
    },
    {
        "source_id": 7,
        "title": "Проекты",
        "url_name": "projects:list",
        "content": "Проекты федерации, программы, статусы, места проведения, контакты и регламенты.",
        "keywords": "проекты программы мероприятия статус контакты",
    },
    {
        "source_id": 8,
        "title": "Медиа",
        "url_name": "media:media_list",
        "content": "Медиа, фотогалереи, фотографии соревнований, проектов и мероприятий.",
        "keywords": "медиа фото фотографии галерея альбом события",
    },
)


def source_key(source_type, source_id):
    return {"source_type": source_type, "source_id": source_id}


def upsert_index(source_type, source_id, **fields):
    fields["title"] = clean_text(fields.get("title"))
    fields["content"] = clean_text(fields.get("content"))
    fields["summary"] = clean_text(fields.get("summary"))
    fields["keywords"] = clean_text(fields.get("keywords"))
    QaIndex.objects.update_or_create(
        **source_key(source_type, source_id),
        defaults=fields,
    )


def delete_index(source_type, source_id):
    QaIndex.objects.filter(**source_key(source_type, source_id)).delete()


def update_static_pages_index():
    for page in STATIC_PAGES:
        upsert_index(
            "page",
            page["source_id"],
            title=page["title"],
            content=page["content"],
            summary=short_text(page["content"]),
            keywords=page["keywords"],
            url=reverse(page["url_name"]),
            is_published=True,
        )


def update_news_index(item):
    if not item.published:
        delete_index("news", item.id)
        return

    full_text = clean_text(item.full_description)
    upsert_index(
        "news",
        item.id,
        title=item.title,
        content=full_text,
        summary=short_text(full_text),
        keywords=f"{item.title} новость новости федерация теннис настольный теннис Курск",
        url=item.get_absolute_url(),
        published_at=item.created_at,
        is_published=True,
    )


def update_project_index(item):
    if not item.is_active or not item.category.is_active:
        delete_index("project", item.id)
        return

    full_text = join_text(
        item.short_description,
        item.full_description,
        item.location,
        item.contacts,
        item.prize_fund,
        item.get_status_display(),
        item.category.title,
        format_date(item.start_date),
        format_date(item.end_date),
        item.external_link,
        item.gallery_link,
    )
    upsert_index(
        "project",
        item.id,
        title=item.title,
        content=full_text,
        summary=short_text(item.short_description or full_text),
        keywords=f"{item.title} проект проекты программа {item.get_status_display()} {item.category.title}",
        url=item.get_absolute_url(),
        is_published=True,
    )


def update_document_category_index(item):
    full_text = join_text(
        item.name,
        "раздел документов категория документы положения регламенты файлы",
    )
    upsert_index(
        "document_category",
        item.id,
        title=item.name,
        content=full_text,
        summary=short_text(full_text, 180),
        keywords=f"{item.name} документы категория положения регламенты",
        url=reverse("documents:category", kwargs={"slug": item.slug}),
        is_published=True,
    )


def update_document_index(item):
    tags = " ".join(item.tags.names())
    full_text = join_text(
        item.title,
        item.description,
        item.category.name,
        tags,
        format_date(item.created_at),
        "документ файл скачать положение регламент материалы федерации",
    )
    upsert_index(
        "document",
        item.id,
        title=item.title,
        content=full_text,
        summary=short_text(item.description or full_text, 220),
        keywords=f"{item.title} {tags} документ документы положение регламент файл скачать",
        url=file_url(item.file) or reverse("documents:category", kwargs={"slug": item.category.slug}),
        published_at=item.created_at,
        is_published=True,
    )


def update_event_index(item):
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
    upsert_index(
        "event",
        item.id,
        title=item.title,
        content=full_text,
        summary=short_text(full_text, 220),
        keywords=f"{item.title} календарь событие события турнир соревнование расписание",
        url=item.pdf_url() or reverse("calendar:calendar"),
        published_at=date_to_datetime(item.start_date),
        is_published=item.is_current,
    )


def update_media_event_index(item):
    full_text = join_text(
        item.title,
        item.description,
        format_date(item.date),
        "медиа фото фотографии фотогалерея галерея альбом соревнования мероприятия",
    )
    upsert_index(
        "media",
        item.id,
        title=item.title,
        content=full_text,
        summary=short_text(item.description or full_text, 220),
        keywords=f"{item.title} медиа фото фотографии галерея альбом",
        url=item.get_absolute_url(),
        published_at=date_to_datetime(item.date),
        is_published=True,
    )


def update_person_index(item):
    if not item.is_active:
        delete_index("person", item.id)
        return

    group = item.get_group_display() if item.group else ""
    full_text = join_text(
        item.full_name,
        item.role,
        group,
        "федерация структура попечительский совет члены федерации руководство",
    )
    upsert_index(
        "person",
        item.id,
        title=item.full_name,
        content=full_text,
        summary=short_text(full_text, 180),
        keywords=f"{item.full_name} {item.role} {group} федерация структура совет",
        url=reverse("structure:structure_home"),
        is_published=True,
    )


def update_partner_index(item):
    full_text = join_text(
        item.name,
        item.url,
        "партнер партнеры спонсор федерации настольного тенниса",
    )
    upsert_index(
        "partner",
        item.id,
        title=item.name,
        content=full_text,
        summary=short_text(full_text, 180),
        keywords=f"{item.name} партнер партнеры спонсор",
        url=item.url or reverse("core:home"),
        is_published=True,
    )


def update_team_member_index(item):
    full_text = join_text(
        item.full_name,
        item.rank,
        item.coach,
        item.get_gender_display() if item.gender else "",
        str(item.rating) if item.rating is not None else "",
        f"сезон {item.season.year}",
        "игрок сборная команда теннис",
    )
    upsert_index(
        "team_member",
        item.id,
        title=item.full_name,
        content=full_text,
        summary=short_text(full_text, 180),
        keywords="игрок сборная теннис команда рейтинг тренер спортсмен",
        url=reverse("teams:teams"),
        is_published=True,
    )


def update_season_index(item):
    full_text = join_text(
        f"Сезон {item.year}",
        "сборная команда игроки список игроков PDF сезон",
    )
    upsert_index(
        "season",
        item.id,
        title=f"Сезон {item.year}",
        content=full_text,
        summary=short_text(full_text, 180),
        keywords=f"сезон {item.year} сборная команда список игроков",
        url=file_url(item.team_list_pdf) or reverse("teams:teams"),
        is_published=True,
    )


def update_coach_index(item):
    full_text = join_text(
        item.full_name,
        item.category,
        "тренер теннис команда",
    )
    upsert_index(
        "coach",
        item.id,
        title=item.full_name,
        content=full_text,
        summary=short_text(full_text, 180),
        keywords="тренер тренеры теннис категория",
        url=reverse("teams:teams"),
        is_published=True,
    )


def update_judge_index(item):
    full_text = join_text(
        item.full_name,
        item.category,
        "судья судьи теннис",
    )
    upsert_index(
        "judge",
        item.id,
        title=item.full_name,
        content=full_text,
        summary=short_text(full_text, 180),
        keywords="судья судьи теннис категория",
        url=reverse("teams:teams"),
        is_published=True,
    )


def update_index_for_instance(instance):
    from core.models import Partner
    from documents.models import Category, Document
    from eventcalendar.models import Event
    from MediaPhoto.models import MediaEvent
    from news.models import News
    from projects.models import Project
    from structure.models import Person
    from teams.models import Coach, Judge, Season, TeamMember

    update_map = {
        News: update_news_index,
        Project: update_project_index,
        Category: update_document_category_index,
        Document: update_document_index,
        Event: update_event_index,
        MediaEvent: update_media_event_index,
        Person: update_person_index,
        Partner: update_partner_index,
        TeamMember: update_team_member_index,
        Season: update_season_index,
        Coach: update_coach_index,
        Judge: update_judge_index,
    }
    update_func = update_map.get(instance.__class__)
    if update_func:
        update_func(instance)


def delete_index_for_instance(instance):
    from core.models import Partner
    from documents.models import Category, Document
    from eventcalendar.models import Event
    from MediaPhoto.models import MediaEvent
    from news.models import News
    from projects.models import Project
    from structure.models import Person
    from teams.models import Coach, Judge, Season, TeamMember

    delete_map = {
        News: "news",
        Project: "project",
        Category: "document_category",
        Document: "document",
        Event: "event",
        MediaEvent: "media",
        Person: "person",
        Partner: "partner",
        TeamMember: "team_member",
        Season: "season",
        Coach: "coach",
        Judge: "judge",
    }
    source_type = delete_map.get(instance.__class__)
    if source_type:
        delete_index(source_type, instance.id)


def rebuild_all():
    from core.models import Partner
    from documents.models import Category, Document
    from eventcalendar.models import Event
    from MediaPhoto.models import MediaEvent
    from news.models import News
    from projects.models import Project
    from structure.models import Person
    from teams.models import Coach, Judge, Season, TeamMember

    QaIndex.objects.all().delete()

    update_static_pages_index()

    for item in News.objects.filter(published=True):
        update_news_index(item)
    for item in Project.objects.filter(is_active=True, category__is_active=True).select_related("category"):
        update_project_index(item)
    for item in Category.objects.all():
        update_document_category_index(item)
    for item in Document.objects.select_related("category").prefetch_related("tags").all():
        update_document_index(item)
    for item in Event.objects.all():
        update_event_index(item)
    for item in MediaEvent.objects.all():
        update_media_event_index(item)
    for item in Person.objects.filter(is_active=True):
        update_person_index(item)
    for item in Partner.objects.all():
        update_partner_index(item)
    for item in TeamMember.objects.select_related("season").all():
        update_team_member_index(item)
    for item in Season.objects.all():
        update_season_index(item)
    for item in Coach.objects.all():
        update_coach_index(item)
    for item in Judge.objects.all():
        update_judge_index(item)

    return QaIndex.objects.count()
