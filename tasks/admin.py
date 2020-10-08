from django.contrib import admin
from .models import Task, ToDoList
# Register your models here.

admin.site.register(Task)
admin.site.register(ToDoList)