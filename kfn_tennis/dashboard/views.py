from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, FormView
from documents.models import Category, Document
from core.models import Partner
from .forms import PartnerForm, CategoryForm, DocumentForm
from .mixins import SuperuserRequiredMixin


class DashboardLoginView(FormView):
    template_name = "dashboard/login.html"
    form_class = AuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return redirect("dashboard:index")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()

        if not user.is_superuser:
            form.add_error(None, "Доступ разрешён только суперпользователю.")
            return self.form_invalid(form)

        login(self.request, user)
        messages.success(self.request, "Вы успешно вошли в панель управления.")

        next_url = self.request.GET.get("next")
        if next_url:
            return HttpResponseRedirect(next_url)

        return redirect("dashboard:index")


def dashboard_logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из панели управления.")
    return redirect("dashboard:login")


class DashboardHomeView(SuperuserRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"


class PartnerListView(SuperuserRequiredMixin, ListView):
    model = Partner
    template_name = "dashboard/partners/list.html"
    context_object_name = "partners"
    paginate_by = 10

    def get_queryset(self):
        queryset = Partner.objects.all().order_by("name")
        search = self.request.GET.get("q", "").strip()
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Партнёры"
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class PartnerCreateView(SuperuserRequiredMixin, CreateView):
    model = Partner
    form_class = PartnerForm
    template_name = "dashboard/partners/form.html"
    success_url = reverse_lazy("dashboard:partner_list")

    def form_valid(self, form):
        messages.success(self.request, "Партнёр успешно создан.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Добавить партнёра"
        context["submit_text"] = "Создать"
        context["cancel_url"] = reverse_lazy("dashboard:partner_list")
        return context


class PartnerUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Partner
    form_class = PartnerForm
    template_name = "dashboard/partners/form.html"
    success_url = reverse_lazy("dashboard:partner_list")

    def form_valid(self, form):
        messages.success(self.request, "Партнёр успешно обновлён.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Редактирование: {self.object.name}"
        context["submit_text"] = "Сохранить"
        context["cancel_url"] = reverse_lazy("dashboard:partner_list")
        return context


class PartnerDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Partner
    template_name = "dashboard/partners/confirm_delete.html"
    success_url = reverse_lazy("dashboard:partner_list")

    def form_valid(self, form):
        messages.success(self.request, "Партнёр успешно удалён.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Удаление: {self.object.name}"
        context["cancel_url"] = reverse_lazy("dashboard:partner_list")
        return context
    
class CategoryListView(SuperuserRequiredMixin, ListView):
    model = Category
    template_name = "dashboard/documents/categories_list.html"
    context_object_name = "categories"
    paginate_by = 10

    def get_queryset(self):
        queryset = Category.objects.all().order_by("order", "name")
        search = self.request.GET.get("q", "").strip()
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Категории документов"
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class CategoryCreateView(SuperuserRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/documents/category_form.html"
    success_url = reverse_lazy("dashboard:category_list")

    def form_valid(self, form):
        messages.success(self.request, "Категория успешно создана.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Добавить категорию"
        context["submit_text"] = "Создать"
        context["cancel_url"] = reverse_lazy("dashboard:category_list")
        return context


class CategoryUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "dashboard/documents/category_form.html"
    success_url = reverse_lazy("dashboard:category_list")

    def form_valid(self, form):
        messages.success(self.request, "Категория успешно обновлена.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Редактирование категории: {self.object.name}"
        context["submit_text"] = "Сохранить"
        context["cancel_url"] = reverse_lazy("dashboard:category_list")
        return context


class CategoryDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Category
    template_name = "dashboard/documents/category_confirm_delete.html"
    success_url = reverse_lazy("dashboard:category_list")

    def form_valid(self, form):
        messages.success(self.request, "Категория успешно удалена.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Удаление категории: {self.object.name}"
        context["cancel_url"] = reverse_lazy("dashboard:category_list")
        return context
    
class DocumentListView(SuperuserRequiredMixin, ListView):
    model = Document
    template_name = "dashboard/documents/documents_list.html"
    context_object_name = "documents"
    paginate_by = 10

    def get_queryset(self):
        queryset = (
            Document.objects.select_related("category")
            .all()
            .order_by("order", "-created_at")
        )
        search = self.request.GET.get("q", "").strip()
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Документы"
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class DocumentCreateView(SuperuserRequiredMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = "dashboard/documents/document_form.html"
    success_url = reverse_lazy("dashboard:document_list")

    def form_valid(self, form):
        messages.success(self.request, "Документ успешно создан.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Добавить документ"
        context["submit_text"] = "Создать"
        context["cancel_url"] = reverse_lazy("dashboard:document_list")
        return context


class DocumentUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = "dashboard/documents/document_form.html"
    success_url = reverse_lazy("dashboard:document_list")

    def form_valid(self, form):
        messages.success(self.request, "Документ успешно обновлён.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Редактирование документа: {self.object.title}"
        context["submit_text"] = "Сохранить"
        context["cancel_url"] = reverse_lazy("dashboard:document_list")
        return context


class DocumentDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Document
    template_name = "dashboard/documents/document_confirm_delete.html"
    success_url = reverse_lazy("dashboard:document_list")

    def form_valid(self, form):
        messages.success(self.request, "Документ успешно удалён.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Удаление документа: {self.object.title}"
        context["cancel_url"] = reverse_lazy("dashboard:document_list")
        return context
    
from eventcalendar.models import Event
from .forms import PartnerForm, CategoryForm, DocumentForm, EventForm

class EventListView(SuperuserRequiredMixin, ListView):
    model = Event
    template_name = "dashboard/calendar/events_list.html"
    context_object_name = "events"
    paginate_by = 10

    def get_queryset(self):
        queryset = Event.objects.all().order_by("-start_date", "-created_at")
        search = self.request.GET.get("q", "").strip()
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Календарь"
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class EventCreateView(SuperuserRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "dashboard/calendar/event_form.html"
    success_url = reverse_lazy("dashboard:event_list")

    def form_valid(self, form):
        messages.success(self.request, "Событие успешно создано.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Добавить событие"
        context["submit_text"] = "Создать"
        context["cancel_url"] = reverse_lazy("dashboard:event_list")
        return context


class EventUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "dashboard/calendar/event_form.html"
    success_url = reverse_lazy("dashboard:event_list")

    def form_valid(self, form):
        messages.success(self.request, "Событие успешно обновлено.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Редактирование события: {self.object.title}"
        context["submit_text"] = "Сохранить"
        context["cancel_url"] = reverse_lazy("dashboard:event_list")
        return context


class EventDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Event
    template_name = "dashboard/calendar/event_confirm_delete.html"
    success_url = reverse_lazy("dashboard:event_list")

    def form_valid(self, form):
        messages.success(self.request, "Событие успешно удалено.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Удаление события: {self.object.title}"
        context["cancel_url"] = reverse_lazy("dashboard:event_list")
        return context