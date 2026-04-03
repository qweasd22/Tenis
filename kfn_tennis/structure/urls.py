from django.urls import path
from . import views

app_name = 'structure'

urlpatterns = [
    path('', views.StructureHomeView.as_view(), name='structure_home'),
    
]
