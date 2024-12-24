from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('notes/', views.notes, name='notes'),
    path('todo/', views.todo, name='todo'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),

    path('update-todo-status/', views.update_todo_status, name='update_todo_status'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('delete_todo/<int:todo_id>/', views.delete_todo, name='delete_todo'),
]