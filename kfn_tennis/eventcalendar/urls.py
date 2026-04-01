from django.urls import path
from .views import calendar_view, calendar_events_json

app_name = 'calendar'

urlpatterns = [
    path('', calendar_view, name='calendar'),
    path('events-json/', calendar_events_json, name='calendar_events_json'),
]
