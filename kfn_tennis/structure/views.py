from django.views.generic import ListView
from .models import Person

class StructureHomeView(ListView):
    model = Person
    template_name = 'structure/structure_home.html'
    context_object_name = 'top_persons'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 7 главных людей для карточек (group='other')
        top_persons = Person.objects.filter(is_active=True, group='other').order_by('id')[:7]
        context['top_persons'] = top_persons

        # Попечительский совет (board)
        context['board_members'] = Person.objects.filter(is_active=True, group='board')

        # Члены федерации (members)
        context['federation_members'] = Person.objects.filter(is_active=True, group='members')

        return context