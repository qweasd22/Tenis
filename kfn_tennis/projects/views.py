from django.views.generic import ListView, DetailView
from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9  # показываем 9 проектов на странице

    def get_queryset(self):
        return Project.objects.filter(
            is_active=True,
            category__is_active=True
        ).select_related('category')

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
