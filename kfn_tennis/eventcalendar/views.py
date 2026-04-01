from django.shortcuts import render
from django.http import JsonResponse
from .models import Event

# Основной календарь
def calendar_view(request):
    return render(request, 'calendar/calendar.html')

from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Event


def calendar_events_json(request):
    events = Event.objects.all()
    data = []

    for event in events:

        # Если есть время — создаём полноценный datetime диапазон
        if event.start_time:
            start = datetime.combine(event.start_date, event.start_time)

            # Если указано окончание
            if event.end_date and event.end_time:
                end = datetime.combine(event.end_date, event.end_time)
            elif event.end_time:
                end = datetime.combine(event.start_date, event.end_time)
            else:
                end = None

            data.append({
                "title": event.title,
                "start": start.isoformat(),
                "end": end.isoformat() if end else None,
                "allDay": False,
                "extendedProps": {
                    "start_date": event.start_date.strftime("%d.%m.%Y"),
                    "end_date": event.end_date.strftime("%d.%m.%Y") if event.end_date else "",
                },
                "url": event.pdf.url if event.pdf else "",
            })

        # Если времени нет — это многодневное allDay
        else:
            end_date = event.end_date or event.start_date

            data.append({
                "title": event.title,
                "start": event.start_date.isoformat(),
                "end": (end_date + timedelta(days=1)).isoformat(),
                "allDay": True,
                "extendedProps": {
                    "start_date": event.start_date.strftime("%d.%m.%Y"),
                    "end_date": end_date.strftime("%d.%m.%Y"),
                },
                "url": event.pdf.url if event.pdf else "",
            })

    return JsonResponse(data, safe=False)
