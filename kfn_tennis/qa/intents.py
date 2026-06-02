def detect_intent(query: str) -> str:
    q = (query or "").lower().replace("ё", "е")

    if any(word in q for word in ["новость", "новости", "последние", "опубликовано"]):
        return "news"

    if any(word in q for word in ["проект", "проекты", "программа"]):
        return "project"

    if any(word in q for word in ["документ", "документы", "положение", "регламент", "приказ", "файл"]):
        return "document"

    if any(word in q for word in ["календар", "событие", "события", "турнир", "соревнован", "расписание"]):
        return "event"

    if any(word in q for word in ["медиа", "фото", "фотограф", "галере", "альбом"]):
        return "media"

    if any(word in q for word in ["федерац", "структур", "попечитель", "совет", "член", "руководств"]):
        return "person"

    if any(word in q for word in ["партнер", "партнеры", "спонсор"]):
        return "partner"

    if any(word in q for word in ["игрок", "игроки", "сборная", "команда", "рейтинг"]):
        return "team_member"

    if any(word in q for word in ["тренер", "тренеры"]):
        return "coach"

    if any(word in q for word in ["судья", "судьи"]):
        return "judge"

    return "general"
