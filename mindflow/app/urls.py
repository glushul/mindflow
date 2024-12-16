from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('notes/', views.notes),
    path('todo/', views.todo),
    path('authorisation/', views.todo),
    path('registration/', views.todo),
]