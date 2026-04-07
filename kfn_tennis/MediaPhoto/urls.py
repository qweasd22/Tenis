from django.urls import path
from . import views

app_name = 'media'

urlpatterns = [
    path('', views.media_list, name='media_list'),
    path('<int:pk>/', views.media_detail, name='media_detail'),
    path('<int:pk>/upload/', views.upload_photos, name='upload_photos'),
]