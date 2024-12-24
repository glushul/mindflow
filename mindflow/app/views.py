import json

from django.contrib.auth import login, get_backends, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .forms import SignupForm, LoginForm, TodoForm, NotesForm
from .models import Note, Todo


#Домашняя страница
def index(request):
    if request.user.is_authenticated:
        return render(request, 'app/index.html', {'authenticated': True})
    else:
        return render(request, 'app/index.html', {'authenticated': False})


#Страница с заметками
@login_required(login_url="/login")
def notes(request):
    form = NotesForm(data=request.POST or None)
    #Если была создана заметка
    if request.method == 'POST':
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('notes')

    #Открытие страницы
    notes = Note.objects.filter(user=request.user).order_by('creation_date', '-creation_time')
    return render(request, 'app/notes.html', {'notes': notes, 'form': form, 'user': request.user.first_name})


#Страница с задачами
@login_required
def todo(request):
    form = TodoForm(data=request.POST or None)
    #Если была создана задача
    if request.method == 'POST':
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo')

    #Получение задач, отсортированных по запланированной дате по убыванию
    todos = Todo.objects.filter(user=request.user).order_by('-planned_date')

    #Группировка всех задач по дате
    todos_grouped_by_date = {}
    for todo in todos:
        date_str = todo.planned_date.strftime("%d.%m.%y")
        if date_str not in todos_grouped_by_date:
            todos_grouped_by_date[date_str] = []
        todos_grouped_by_date[date_str].append({
            'id': todo.id,
            'text': todo.text,
            'planned_time': todo.planned_time.strftime("%H:%M"),
            'done': todo.done,
        })

    #Сортировка задач по времени
    todos_data = [
        {
            'planned_date': date,
            'todos': sorted(todos_grouped_by_date[date], key=lambda todo: todo['planned_time'])
        }
        for date in todos_grouped_by_date
    ]

    # Открытие страницы
    return render(request, 'app/todo.html', {'todos_data': todos_data, 'form': form, 'user': request.user.first_name})


#Страница входа
def login_view(request):
    form = LoginForm(data=request.POST or None)
    #Если пользователь попытался войти
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request=request, user=user)
            return redirect('/todo')

    #Открытие страницы
    return render(request, 'app/login.html', {'form': form})


#Страница регистрации
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Этот email уже используется.')
            else:
                try:
                    user = form.save(commit=False)
                    user.username = email
                    user.save()
                    backend = get_backends()[0]
                    user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
                    login(request, user)
                    return redirect('/todo')
                except IntegrityError:
                    form.add_error('username', 'Пользователь с таким именем уже существует.')
    else:
        form = SignupForm()

    #Открытие страницы
    return render(request, 'app/signup.html', {"form": form})


#Обновление статуса задачи (done: True|False)
@csrf_exempt
def update_todo_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            todo_id = data.get('todo_id')
            done = data.get('done')

            todo = Todo.objects.get(id=todo_id)

            todo.done = done
            todo.save()

            return JsonResponse({'success': True})

        except Todo.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == "POST":
        note.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)

    if request.method == "POST":
        todo.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)