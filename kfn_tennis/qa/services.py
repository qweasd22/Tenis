import re

from qa.models import QaIndex
from qa.intents import detect_intent


def normalize_text(text: str) -> str:
    text = (text or "").lower().replace("ё", "е")
    text = re.sub(r"[^a-zа-я0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> list[str]:
    return [w for w in normalize_text(text).split() if len(w) > 1]


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


def calc_score(query_words, item, source_boost=0):
    title = normalize_text(item.title)
    content = normalize_text(item.content)
    summary = normalize_text(item.summary)
    keywords = normalize_text(item.keywords)

    score = source_boost

    for word in query_words:
        variants = word_variants(word)

        for v in variants:
            if v in title:
                score += 8
            if v in keywords:
                score += 6
            if v in summary:
                score += 4
            if v in content:
                score += 2

    full_query = " ".join(query_words)
    if full_query and full_query in title:
        score += 15
    if full_query and full_query in summary:
        score += 10
    if full_query and full_query in content:
        score += 5

    return score


def search_qa(query: str):
    query_words = tokenize(query)
    if not query_words:
        return []

    intent = detect_intent(query)

    items = QaIndex.objects.filter(is_published=True)

    source_priority = {
        "news": {"news": 20},
        "project": {"project": 20},
        "team_member": {"team_member": 20},
        "coach": {"coach": 20},
        "judge": {"judge": 20},
        "general": {},
    }

    boosts = source_priority.get(intent, {})
    scored = []

    for item in items:
        source_boost = boosts.get(item.source_type, 0)
        score = calc_score(query_words, item, source_boost=source_boost)
        if score > 0:
            scored.append((score, item))

    if intent == "news":
        scored.sort(
            key=lambda x: (x[0], x[1].published_at.timestamp() if x[1].published_at else 0),
            reverse=True
        )
    else:
        scored.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in scored[:5]]

def build_answer(query: str, results):
    if not results:
        return {
            "text": "По вашему запросу ничего не найдено.",
            "top_result": None,
        }

    first = results[0]

    if first.source_type == "news":
        text = f"Найдена подходящая новость: {first.title}"
    elif first.source_type == "project":
        text = f"Найден подходящий проект: {first.title}"
    elif first.source_type == "team_member":
        text = f"Найден игрок: {first.title}"
    elif first.source_type == "coach":
        text = f"Найден тренер: {first.title}"
    elif first.source_type == "judge":
        text = f"Найден судья: {first.title}"
    else:
        text = f"Найден материал: {first.title}"

    return {
        "text": text,
        "top_result": first,
    }