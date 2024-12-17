from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Todo, Note


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

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))

class TodoForm(forms.ModelForm):
    planned_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    planned_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Todo
        fields = ['text', 'planned_date', 'planned_time']

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


class NotesForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ['text']