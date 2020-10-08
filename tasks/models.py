from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    background = models.CharField(default='linear-gradient(to top, #48c6ef 0%, #6f86d6 100%)', max_length=300)

class ToDoList(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name='to_do_lists')
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

class Task(models.Model):
    task_name = models.CharField(max_length=100)
    to_do_list = models.ForeignKey("ToDoList", on_delete=models.CASCADE, related_name='tasks')
    importance = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    time_start = models.TimeField(blank=True)
    time_end = models.TimeField(blank=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.task_name}'
