def detect_intent(query: str) -> str:
    q = (query or "").lower()

    if any(word in q for word in ["новость", "новости", "последние", "опубликовано"]):
        return "news"

    if any(word in q for word in ["проект", "проекты", "программа"]):
        return "project"

    if any(word in q for word in ["игрок", "игроки", "сборная", "команда", "рейтинг"]):
        return "team_member"

    if any(word in q for word in ["тренер", "тренеры"]):
        return "coach"

    if any(word in q for word in ["судья", "судьи"]):
        return "judge"

    return "general"