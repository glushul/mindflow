from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    text = models.CharField(max_length=2000)
    creation_date = models.DateField(auto_now_add=True)
    creation_time = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Note for {self.user.username}"

    class Meta:
        db_table = 'app_note'

class Todo(models.Model):
    text = models.CharField(max_length=2000)
    planned_date = models.DateField()
    planned_time = models.TimeField()
    done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Todo for {self.user.username}"

    class Meta:
        db_table = 'app_todo'