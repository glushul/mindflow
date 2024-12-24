from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Todo, Note


#Форма входа
class SignupForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="First Name")
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


#Форма регистрации
class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))


#Форма добавления задач
class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ['text', 'planned_date', 'planned_time']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'todo-input',
                'rows': 4,
                'cols': 50,
                'placeholder': 'Запланируйте что-нибудь...',
                'id': 'autoResizeTextarea',
            }),
            'planned_date': forms.DateInput(attrs={
                'class': 'data-btn',
                'placeholder': 'Выберите дату',
                'type': 'date',
            }),
            'planned_time': forms.TimeInput(attrs={
                'class': 'data-btn',
                'placeholder': 'Выберите время',
                'type': 'time',
            }, format='%H:%M'),
        }
        labels = {
            'planned_date': '',
            'planned_time': '',
            'text': '',
        }

    def clean_planned_date(self):
        planned_date = self.cleaned_data.get('planned_date')
        if not planned_date:
            raise forms.ValidationError("Пожалуйста, выберите дату.")

        if planned_date < timezone.localdate():
            raise ValidationError("Дата не может быть в прошлом.")

        return planned_date

    def clean_planned_time(self):
        planned_time = self.cleaned_data.get('planned_time')
        planned_date = self.cleaned_data.get('planned_date')

        if not planned_time:
            raise forms.ValidationError("Пожалуйста, выберите время.")

        if not planned_date:
            raise forms.ValidationError("Пожалуйста, выберите дату.")

        planned_datetime = timezone.make_aware(
            timezone.datetime.combine(planned_date, planned_time)
        )

        if planned_datetime < timezone.now():
            if planned_date == timezone.localdate() and planned_time < timezone.localtime().time():
                raise ValidationError("Время не может быть в прошлом.")

            raise ValidationError("Время не может быть в прошлом.")

        return planned_time


#Форма добавления заметок
class NotesForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'note-input',
                'rows': 4,
                'cols': 50,
                'placeholder': 'Напишите что-нибудь...',
                'id': 'autoResizeTextarea',
            }),
        }
        labels = {
            'text': '',
        }