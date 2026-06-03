import re

from qa.models import QaIndex
from qa.intents import detect_intent


SEARCH_LIMIT = 10

STOP_WORDS = {
    "где", "как", "что", "кто", "куда", "когда", "какие", "какой", "какая",
    "найти", "найди", "есть", "про", "по", "на", "в", "и", "или", "для",
    "мне", "сайт", "сайте", "показать", "покажи", "посмотреть", "открыть",
}

SOFT_WORDS = {
    "последние", "последняя", "последний", "свежие", "свежая", "свежий",
    "актуальные", "актуальная", "актуальный", "новые", "новая", "новый",
}

INTENT_WORDS = {
    "новость", "новости",
    "документ", "документы", "положение", "регламент", "приказ", "файл",
    "медиа", "фото", "фотография", "фотографии", "галерея", "альбом",
    "календарь", "событие", "события", "турнир", "турниры", "соревнование", "соревнования", "расписание",
    "проект", "проекты", "программа",
    "федерация", "структура", "попечительский", "совет", "член", "члены", "руководство",
    "партнер", "партнеры", "спонсор",
    "игрок", "игроки", "сборная", "команда", "рейтинг",
    "тренер", "тренеры",
    "судья", "судьи",
}

SOURCE_PRIORITY = {
    "news": {"news": 42, "page": -8},
    "project": {"project": 38, "page": 4},
    "document": {"document": 42, "document_category": 24, "page": 2},
    "event": {"event": 42, "page": 4, "news": 4, "project": 2},
    "media": {"media": 42, "page": 4, "event": -8},
    "person": {"person": 42, "page": 4},
    "partner": {"partner": 42, "page": 4},
    "team_member": {"team_member": 40, "coach": 8, "judge": 4, "season": 10, "page": 2},
    "coach": {"coach": 42, "team_member": 10, "page": 2},
    "judge": {"judge": 42, "page": 2},
    "general": {},
}

TYPE_LABELS = {
    "news": "новость",
    "project": "проект",
    "document": "документ",
    "document_category": "раздел документов",
    "event": "событие",
    "media": "медиаматериал",
    "person": "участник федерации",
    "partner": "партнер",
    "season": "сезон сборной",
    "team_member": "игрок",
    "coach": "тренер",
    "judge": "судья",
    "page": "раздел сайта",
}

NAVIGATION_WORDS = {"где", "куда", "открыть", "перейти", "раздел", "страница", "ссылка"}


def normalize_text(text: str) -> str:
    text = (text or "").lower().replace("ё", "е")
    text = re.sub(r"[^a-zа-я0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list[str]:
    return [w for w in normalize_text(text).split() if len(w) > 1 and w not in STOP_WORDS]


def word_variants(word: str) -> set[str]:
    variants = {word}
    endings = [
        "ами", "ями", "ого", "ему", "ому", "иях", "ах", "ях",
        "ий", "ый", "ой", "ая", "яя", "ое", "ее",
        "ов", "ев", "ей", "ам", "ям", "ом", "ем",
        "а", "я", "ы", "и", "е", "у", "ю", "о"
    ]
    for ending in endings:
        if word.endswith(ending) and len(word) > len(ending) + 2:
            variants.add(word[:-len(ending)])
    return {v for v in variants if len(v) > 1}


def field_tokens(text: str) -> set[str]:
    return set(normalize_text(text).split())


def is_intent_only_word(word: str) -> bool:
    variants = word_variants(word)
    return word in SOFT_WORDS or any(variant in INTENT_WORDS for variant in variants)


def required_words(query_words: list[str]) -> list[str]:
    return [word for word in query_words if not is_intent_only_word(word)]


def has_navigation_intent(query: str) -> bool:
    tokens = set(normalize_text(query).split())
    return bool(tokens & NAVIGATION_WORDS)


def field_match_score(word: str, normalized_field: str, tokens: set[str], exact_weight: int, stem_weight: int, substring_weight: int) -> int:
    variants = word_variants(word)
    score = 0

    if word in tokens:
        score = max(score, exact_weight)

    if any(variant in tokens for variant in variants):
        score = max(score, stem_weight)

    if len(word) >= 4 and any(variant in normalized_field for variant in variants):
        score = max(score, substring_weight)

    return score


def calc_score(query_words, item, source_boost=0):
    fields = {
        "title": normalize_text(item.title),
        "content": normalize_text(item.content),
        "summary": normalize_text(item.summary),
        "keywords": normalize_text(item.keywords),
    }
    tokens = {name: field_tokens(value) for name, value in fields.items()}

    score = source_boost
    matched_words = set()
    required = required_words(query_words)

    for word in query_words:
        word_score = 0
        word_score += field_match_score(word, fields["title"], tokens["title"], 18, 13, 6)
        word_score += field_match_score(word, fields["keywords"], tokens["keywords"], 11, 8, 4)
        word_score += field_match_score(word, fields["summary"], tokens["summary"], 7, 5, 3)
        word_score += field_match_score(word, fields["content"], tokens["content"], 4, 3, 1)

        if word_score:
            matched_words.add(word)
            score += word_score

    full_query = " ".join(query_words)
    if full_query and full_query in fields["title"]:
        score += 32
    if full_query and full_query in fields["summary"]:
        score += 18
    if full_query and full_query in fields["content"]:
        score += 10

    if required and not any(word in matched_words for word in required):
        return 0

    if query_words:
        coverage = len(matched_words) / len(query_words)
        score += int(coverage * 12)

    if len(required) >= 2 and all(word in matched_words for word in required):
        score += 16

    if item.source_type == "page" and item.title.lower() not in " ".join(query_words):
        score -= 12

    return score


def search_qa(query: str):
    query_words = tokenize(query)
    if not query_words:
        return []

    intent = detect_intent(query)

    items = QaIndex.objects.filter(is_published=True)

    boosts = SOURCE_PRIORITY.get(intent, {})
    required = required_words(query_words)
    if has_navigation_intent(query) and not required:
        boosts = {**boosts, "page": max(boosts.get("page", 0), 48)}
    scored = []

    for item in items:
        source_boost = boosts.get(item.source_type, 0)
        score = calc_score(query_words, item, source_boost=source_boost)
        if score > 0:
            source_tier = 1 if source_boost > 0 else -1 if source_boost < 0 else 0
            scored.append((source_tier, score, item))

    scored.sort(
        key=lambda x: (
            x[0],
            x[1],
            x[2].published_at.timestamp() if x[2].published_at else 0,
            x[2].id,
        ),
        reverse=True
    )

    return [item for source_tier, score, item in scored[:SEARCH_LIMIT]]


def build_answer(query: str, results):
    if not results:
        return {
            "text": "По вашему запросу ничего не найдено.",
            "top_result": None,
        }

    first = results[0]

    label = TYPE_LABELS.get(first.source_type, "материал")
    if len(results) == 1:
        text = f"Нашёл подходящий {label}: {first.title}"
    else:
        text = f"Лучшее совпадение — {label}: {first.title}. Ещё {len(results) - 1} результатов ниже."

    return {
        "text": text,
        "top_result": first,
    }
