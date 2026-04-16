from django.urls import path
from .views import qa_page, qa_ask

app_name = "qa"

urlpatterns = [
    path("", qa_page, name="qa_page"),
    path("ask/", qa_ask, name="qa_ask"),
]