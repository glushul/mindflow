from django.shortcuts import render


def index(request):
    return render(request, 'app/index.html')

def notes(request):
    return render(request, 'app/notes.html')

def todo(request):
    return render(request, 'app/todo.html')

def authorization(request):
    return render(request, 'app/authorisation.html')

def registration(request):
    return render(request, 'app/registration.html')