from django.urls import path
from .views import (
    DashboardHomeView,
    DashboardLoginView,
    dashboard_logout_view,
    PartnerListView,
    PartnerCreateView,
    PartnerUpdateView,
    PartnerDeleteView,
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    DocumentListView,
    DocumentCreateView,
    DocumentUpdateView,
    DocumentDeleteView,
    EventListView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
)

app_name = "dashboard"

urlpatterns = [
    path("login/", DashboardLoginView.as_view(), name="login"),
    path("logout/", dashboard_logout_view, name="logout"),
    path("", DashboardHomeView.as_view(), name="index"),

    path("partners/", PartnerListView.as_view(), name="partner_list"),
    path("partners/create/", PartnerCreateView.as_view(), name="partner_create"),
    path("partners/<int:pk>/edit/", PartnerUpdateView.as_view(), name="partner_update"),
    path("partners/<int:pk>/delete/", PartnerDeleteView.as_view(), name="partner_delete"),

    path("documents/categories/", CategoryListView.as_view(), name="category_list"),
    path("documents/categories/create/", CategoryCreateView.as_view(), name="category_create"),
    path("documents/categories/<int:pk>/edit/", CategoryUpdateView.as_view(), name="category_update"),
    path("documents/categories/<int:pk>/delete/", CategoryDeleteView.as_view(), name="category_delete"),
    path("documents/", DocumentListView.as_view(), name="document_list"),
    path("documents/create/", DocumentCreateView.as_view(), name="document_create"),
    path("documents/<int:pk>/edit/", DocumentUpdateView.as_view(), name="document_update"),
    path("documents/<int:pk>/delete/", DocumentDeleteView.as_view(), name="document_delete"),

    path("calendar/", EventListView.as_view(), name="event_list"),
    path("calendar/create/", EventCreateView.as_view(), name="event_create"),
    path("calendar/<int:pk>/edit/", EventUpdateView.as_view(), name="event_update"),
    path("calendar/<int:pk>/delete/", EventDeleteView.as_view(), name="event_delete"),
]