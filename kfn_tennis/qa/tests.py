from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from core.templatetags.public_extras import clean_text
from documents.models import Category, Document
from news.models import News
from qa.indexers import format_date_range
from qa.models import QaIndex
from qa.services import build_answer, search_qa


class QaSearchTests(TestCase):
    def test_qa_page_uses_public_site_layout(self):
        response = self.client.get("/qa/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "site-header")
        self.assertContains(response, "qa-search-page")

    def test_search_prioritizes_document_intent(self):
        document = QaIndex.objects.create(
            source_type="document",
            source_id=1,
            title="Положение о турнире",
            content="Официальный регламент соревнования",
            summary="Регламент соревнования",
            keywords="документ положение регламент турнир",
            url="/media/documents/reglament.pdf",
        )
        QaIndex.objects.create(
            source_type="news",
            source_id=1,
            title="Новость о турнире",
            content="Итоги соревнования",
            summary="Итоги турнира",
            keywords="новость турнир",
            url="/news/tournament/",
        )

        results = search_qa("где найти положение турнира")

        self.assertEqual(results[0], document)

    def test_search_covers_calendar_media_and_structure(self):
        event = QaIndex.objects.create(
            source_type="event",
            source_id=1,
            title="Кубок Курска",
            content="Календарь соревнований расписание турнир",
            keywords="календарь событие соревнование",
            url="/eventcalendar/",
        )
        media = QaIndex.objects.create(
            source_type="media",
            source_id=1,
            title="Фото Кубка Курска",
            content="Фотогалерея соревнования",
            keywords="медиа фото галерея",
            url="/media/1/",
        )
        person = QaIndex.objects.create(
            source_type="person",
            source_id=1,
            title="Иван Иванов",
            content="Попечительский совет федерации",
            keywords="структура федерация совет",
            url="/structure/",
        )

        self.assertEqual(search_qa("расписание соревнований")[0], event)
        self.assertEqual(search_qa("фото соревнований")[0], media)
        self.assertEqual(search_qa("попечительский совет")[0], person)

    def test_build_answer_uses_new_source_labels(self):
        result = QaIndex.objects.create(
            source_type="media",
            source_id=1,
            title="Финал сезона",
            content="Фотогалерея",
            url="/media/1/",
        )

        answer = build_answer("фото финала", [result])

        self.assertEqual(answer["top_result"], result)
        self.assertIn("медиаматериал", answer["text"])

    def test_format_date_range_allows_empty_end_date(self):
        self.assertEqual(format_date_range(date(2026, 6, 2), None), "02.06.2026")

    def test_latest_news_prefers_news_item_over_section_page(self):
        page = QaIndex.objects.create(
            source_type="page",
            source_id=1,
            title="Новости",
            content="Все опубликованные новости федерации.",
            keywords="новости публикации объявления",
            url="/news/",
        )
        news = QaIndex.objects.create(
            source_type="news",
            source_id=2,
            title="Открыт новый сезон",
            content="Подробности открытия сезона.",
            keywords="новость новости федерация",
            url="/news/new-season/",
        )

        results = search_qa("последние новости")

        self.assertEqual(results[0], news)
        self.assertIn(page, results)

    def test_photo_query_prefers_media_over_calendar_event(self):
        media = QaIndex.objects.create(
            source_type="media",
            source_id=1,
            title="Фото чемпионата",
            content="Фотографии соревнования",
            keywords="медиа фото галерея соревнования",
            url="/media/1/",
        )
        QaIndex.objects.create(
            source_type="event",
            source_id=1,
            title="Чемпионат области",
            content="Календарь соревнования",
            keywords="календарь событие соревнование",
            url="/eventcalendar/",
        )

        self.assertEqual(search_qa("фото соревнований")[0], media)

    def test_specific_coach_query_filters_generic_coaches(self):
        coach = QaIndex.objects.create(
            source_type="coach",
            source_id=1,
            title="Камардин Сергей Владимирович",
            content="тренер теннис команда",
            keywords="тренер тренеры теннис",
            url="/teams/",
        )
        QaIndex.objects.create(
            source_type="coach",
            source_id=2,
            title="Иванов Иван Иванович",
            content="тренер теннис команда",
            keywords="тренер тренеры теннис",
            url="/teams/",
        )

        results = search_qa("тренер камардина")

        self.assertEqual(results, [coach])

    def test_navigation_query_prefers_section_page(self):
        page = QaIndex.objects.create(
            source_type="page",
            source_id=4,
            title="Документы",
            content="Официальные документы федерации.",
            keywords="документы положения регламенты",
            url="/documents/",
        )
        QaIndex.objects.create(
            source_type="document_category",
            source_id=1,
            title="Нормативные документы",
            content="раздел документов",
            keywords="документы категория",
            url="/documents/normative/",
        )

        self.assertEqual(search_qa("где документы")[0], page)


class QaAutoIndexTests(TestCase):
    def test_news_save_and_unpublish_refreshes_index(self):
        news = News.objects.create(
            title="Новая секция настольного тенниса",
            slug="new-section",
            full_description="Открыта новая секция для юных спортсменов.",
            published=True,
        )

        index_item = QaIndex.objects.get(source_type="news", source_id=news.id)
        self.assertEqual(index_item.title, news.title)

        news.published = False
        news.save()

        self.assertFalse(QaIndex.objects.filter(source_type="news", source_id=news.id).exists())

    def test_document_tags_change_refreshes_index(self):
        category = Category.objects.create(name="Регламенты", slug="reglaments")
        document = Document.objects.create(
            title="Положение о соревнованиях",
            description="Основные правила проведения соревнований.",
            category=category,
            file=SimpleUploadedFile("rules.pdf", b"pdf"),
        )

        document.tags.add("дети")

        index_item = QaIndex.objects.get(source_type="document", source_id=document.id)
        self.assertIn("дети", index_item.keywords)


class PublicTextFiltersTests(TestCase):
    def test_clean_text_decodes_nbsp_entity(self):
        self.assertEqual(clean_text("Последние&nbsp;новости&nbsp;&mdash; итог"), "Последние новости — итог")
