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
    
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from MediaPhoto.models import MediaEvent, MediaPhoto
from MediaPhoto.forms import MultiUploadForm
from .forms import PartnerForm, CategoryForm, DocumentForm, EventForm, MediaEventForm

class MediaEventListView(SuperuserRequiredMixin, ListView):
    model = MediaEvent
    template_name = "dashboard/media/events_list.html"
    context_object_name = "events"
    paginate_by = 10

    def get_queryset(self):
        queryset = MediaEvent.objects.all().order_by("-date")
        search = self.request.GET.get("q", "").strip()
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Медиа"
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class MediaEventCreateView(SuperuserRequiredMixin, CreateView):
    model = MediaEvent
    form_class = MediaEventForm
    template_name = "dashboard/media/event_form.html"
    success_url = reverse_lazy("dashboard:media_event_list")

    def form_valid(self, form):
        messages.success(self.request, "Медиа-мероприятие успешно создано.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Добавить медиа-мероприятие"
        context["submit_text"] = "Создать"
        context["cancel_url"] = reverse_lazy("dashboard:media_event_list")
        return context


class MediaEventUpdateView(SuperuserRequiredMixin, UpdateView):
    model = MediaEvent
    form_class = MediaEventForm
    template_name = "dashboard/media/event_form.html"
    success_url = reverse_lazy("dashboard:media_event_list")

    def form_valid(self, form):
        messages.success(self.request, "Медиа-мероприятие успешно обновлено.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Редактирование: {self.object.title}"
        context["submit_text"] = "Сохранить"
        context["cancel_url"] = reverse_lazy("dashboard:media_event_list")
        return context


class MediaEventDeleteView(SuperuserRequiredMixin, DeleteView):
    model = MediaEvent
    template_name = "dashboard/media/event_confirm_delete.html"
    success_url = reverse_lazy("dashboard:media_event_list")

    def form_valid(self, form):
        messages.success(self.request, "Медиа-мероприятие успешно удалено.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Удаление: {self.object.title}"
        context["cancel_url"] = reverse_lazy("dashboard:media_event_list")
        return context


class MediaEventPhotosView(SuperuserRequiredMixin, TemplateView):
    template_name = "dashboard/media/event_photos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = get_object_or_404(MediaEvent, pk=self.kwargs["pk"])
        context["event"] = event
        context["photos"] = event.photos.all().order_by("-uploaded_at")
        context["upload_form"] = MultiUploadForm()
        context["page_title"] = f"Фотографии: {event.title}"
        return context


class MediaPhotoUploadView(SuperuserRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(MediaEvent, pk=pk)
        form = MultiUploadForm(request.POST, request.FILES)

        if form.is_valid():
            files = request.FILES.getlist("images")
            for f in files:
                MediaPhoto.objects.create(event=event, image=f)
            messages.success(request, f"Загружено файлов: {len(files)}.")
        else:
            messages.error(request, "Не удалось загрузить фотографии.")

        return redirect("dashboard:media_event_photos", pk=pk)


class MediaPhotoDeleteView(SuperuserRequiredMixin, View):
    def post(self, request, pk, photo_pk):
        event = get_object_or_404(MediaEvent, pk=pk)
        photo = get_object_or_404(MediaPhoto, pk=photo_pk, event=event)
        photo.delete()
        messages.success(request, "Фотография удалена.")
        return redirect("dashboard:media_event_photos", pk=pk)

from news.models import News
from .forms import  NewsForm

class DashboardNewsListView(SuperuserRequiredMixin, ListView):
    model = News
    template_name = "dashboard/news/news_list.html"
    context_object_name = "news_items"
    paginate_by = 10

    def get_queryset(self):
        queryset = News.objects.all().order_by("-created_at")
        search = self.request.GET.get("q", "").strip()
        if search:
            queryset = queryset.filter(
                title__icontains=search
            ) | queryset.filter(
                full_description__icontains=search
            )
            queryset = queryset.order_by("-created_at")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Новости"
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class DashboardNewsCreateView(SuperuserRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    template_name = "dashboard/news/news_form.html"
    success_url = reverse_lazy("dashboard:news_list")

    def form_valid(self, form):
        messages.success(self.request, "Новость успешно создана.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Добавить новость"
        context["submit_text"] = "Создать"
        context["cancel_url"] = reverse_lazy("dashboard:news_list")
        return context


class DashboardNewsUpdateView(SuperuserRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = "dashboard/news/news_form.html"
    success_url = reverse_lazy("dashboard:news_list")

    def form_valid(self, form):
        messages.success(self.request, "Новость успешно обновлена.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Редактирование: {self.object.title}"
        context["submit_text"] = "Сохранить"
        context["cancel_url"] = reverse_lazy("dashboard:news_list")
        return context


class DashboardNewsDeleteView(SuperuserRequiredMixin, DeleteView):
    model = News
    template_name = "dashboard/news/news_confirm_delete.html"
    success_url = reverse_lazy("dashboard:news_list")

    def form_valid(self, form):
        messages.success(self.request, "Новость успешно удалена.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Удаление: {self.object.title}"
        context["cancel_url"] = reverse_lazy("dashboard:news_list")
        return context

from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect
from projects.models import ProjectCategory, Project
from .forms import PartnerForm, CategoryForm, DocumentForm, EventForm, MediaEventForm, NewsForm, ProjectCategoryForm, ProjectForm

class ProjectCategoryListView(SuperuserRequiredMixin, ListView):
    model = ProjectCategory
    template_name = "dashboard/projects/categories_list.html"
    context_object_name = "categories"
    paginate_by = 10

    def get_queryset(self):
        queryset = ProjectCategory.objects.all().order_by("order", "title")
        search = self.request.GET.get("q", "").strip()
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Категории проектов"
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class ProjectCategoryCreateView(SuperuserRequiredMixin, CreateView):
    model = ProjectCategory
    form_class = ProjectCategoryForm
    template_name = "dashboard/projects/category_form.html"
    success_url = reverse_lazy("dashboard:project_category_list")

    def form_valid(self, form):
        messages.success(self.request, "Категория проекта успешно создана.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Добавить категорию проекта"
        context["submit_text"] = "Создать"
        context["cancel_url"] = reverse_lazy("dashboard:project_category_list")
        return context


class ProjectCategoryUpdateView(SuperuserRequiredMixin, UpdateView):
    model = ProjectCategory
    form_class = ProjectCategoryForm
    template_name = "dashboard/projects/category_form.html"
    success_url = reverse_lazy("dashboard:project_category_list")

    def form_valid(self, form):
        messages.success(self.request, "Категория проекта успешно обновлена.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Редактирование категории: {self.object.title}"
        context["submit_text"] = "Сохранить"
        context["cancel_url"] = reverse_lazy("dashboard:project_category_list")
        return context


class ProjectCategoryDeleteView(SuperuserRequiredMixin, DeleteView):
    model = ProjectCategory
    template_name = "dashboard/projects/category_confirm_delete.html"
    success_url = reverse_lazy("dashboard:project_category_list")

    def form_valid(self, form):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(self.request, "Категория проекта успешно удалена.")
        except ProtectedError:
            messages.error(
                self.request,
                "Нельзя удалить категорию, пока к ней привязаны проекты."
            )
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Удаление категории: {self.object.title}"
        context["cancel_url"] = reverse_lazy("dashboard:project_category_list")
        return context

class DashboardProjectListView(SuperuserRequiredMixin, ListView):
    model = Project
    template_name = "dashboard/projects/projects_list.html"
    context_object_name = "projects"
    paginate_by = 10

    def get_queryset(self):
        queryset = Project.objects.select_related("category").all().order_by("order", "-start_date")
        search = self.request.GET.get("q", "").strip()
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(short_description__icontains=search) |
                Q(category__title__icontains=search)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Проекты"
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context


class DashboardProjectCreateView(SuperuserRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "dashboard/projects/project_form.html"
    success_url = reverse_lazy("dashboard:project_list")

    def form_valid(self, form):
        messages.success(self.request, "Проект успешно создан.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Добавить проект"
        context["submit_text"] = "Создать"
        context["cancel_url"] = reverse_lazy("dashboard:project_list")
        return context


class DashboardProjectUpdateView(SuperuserRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "dashboard/projects/project_form.html"
    success_url = reverse_lazy("dashboard:project_list")

    def form_valid(self, form):
        messages.success(self.request, "Проект успешно обновлён.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Редактирование: {self.object.title}"
        context["submit_text"] = "Сохранить"
        context["cancel_url"] = reverse_lazy("dashboard:project_list")
        return context


class DashboardProjectDeleteView(SuperuserRequiredMixin, DeleteView):
    model = Project
    template_name = "dashboard/projects/project_confirm_delete.html"
    success_url = reverse_lazy("dashboard:project_list")

    def form_valid(self, form):
        messages.success(self.request, "Проект успешно удалён.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Удаление: {self.object.title}"
        context["cancel_url"] = reverse_lazy("dashboard:project_list")
        return context