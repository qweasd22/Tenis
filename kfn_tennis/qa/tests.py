from django.test import TestCase

from qa.management.commands.rebuild_qa_index import format_date_range
from qa.models import QaIndex
from qa.services import build_answer, search_qa


class QaSearchTests(TestCase):
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
        from datetime import date

        self.assertEqual(format_date_range(date(2026, 6, 2), None), "02.06.2026")
