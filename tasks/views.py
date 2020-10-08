from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.template.defaulttags import register

# Create your views here.
from .models import User, ToDoList, Task

def index(request):
    return render(request, 'tasks/index.html')

@register.filter
def get_range(value):
    return range(value)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('tasks:index'))
        else:
            return render(request, 'tasks/login.html', {
                'error_message':'Invalid credentials.'
            })
    else:
        return render(request, 'tasks/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('tasks:index'))

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        
        if password != confirm_password:
            return render(request, 'tasks/register.html', {'error_message':'Password must match.'})

        new_user = User.objects.create_user(username,email,password)
        new_user.save()
        login(request, new_user)
        return render(request, 'tasks/index.html', {'success_message':'Registration successful!'})
        
    return render(request, 'tasks/register.html')

def contact(request):
    return render(request, 'tasks/contact.html')

@login_required
def active_lists(request):
    user = request.user
    active_lists = user.to_do_lists.filter(archived=False).all()
    return render(request, 'tasks/active_lists.html', {'active_lists':active_lists})

@login_required
def archived_lists(request):
    user = request.user
    archived_lists = user.to_do_lists.filter(archived=True).all()
    return render(request, 'tasks/archived_lists.html', {'archived_lists':archived_lists})

@login_required
def create_list(request):
    if request.method == 'POST':
        list_name = request.POST['list-name']
        try:
            new_list = ToDoList.objects.create(author=request.user, name=list_name)
            new_list.save()
            messages.success(request, 'List created!')
            return HttpResponseRedirect(reverse('tasks:active_lists'))
        except:
            context = {
                'error_message':f'There was an issue creating your List {list_name}'
            }
            return render(request, 'tasks/create_list.html', context)

    return render(request, 'tasks/create_list.html')

@login_required
def list_page(request, list_id):
    if request.method == 'POST':
        if 'done-task' in request.POST:
            task_id = request.POST['task-done']
            try:
                task = Task.objects.get(pk=int(task_id))
                task.done = True
                task.save()

                current_list = ToDoList.objects.get(pk=list_id)
                context = {
                    'success_message':f'Task done {task}!',
                    'list': current_list,
                    'tasks':current_list.tasks.all()
                }
                return render(request, 'tasks/list_page.html', context)
            except:
                current_list = ToDoList.objects.get(pk=list_id)
                context = {
                    'error_message':f'There was an issue, {task_name}',
                    'list': current_list,
                    'tasks':current_list.tasks.all()
                }
                return render(request, 'tasks/list_page.html', context)
            
        if 'archive-list' in request.POST:
            to_do_list = ToDoList.objects.get(pk=list_id)
            if to_do_list.archived == True:
                to_do_list.archived = False
            else:
                to_do_list.archived = True
            to_do_list.save()

            user = request.user
            active_lists = user.to_do_lists.filter(archived=False).all()
            context = {
                    'success_message':f'List status changed!',
                    'active_lists':active_lists
            }
            return render(request, 'tasks/active_lists.html', context)
            
        if 'add-task' in request.POST:
            task_name = request.POST['task-name']
            to_do_list = ToDoList.objects.get(pk=list_id)
            importance = request.POST['importance']
            time_start = request.POST['time-start']
            time_end = request.POST['time-end']
            try:
                new_task = Task.objects.create(
                    task_name=task_name,
                    to_do_list=to_do_list,
                    importance=importance,
                    time_start=time_start,
                    time_end=time_end
                )
                new_task.save()
                messages.success(request, 'Task saved!')
                return HttpResponseRedirect(reverse("task:list_page",args=[to_do_list.id]))
            except:
                current_list = ToDoList.objects.get(pk=list_id)
                context = {
                    'error_message':'There was an issue creating your Task',
                    'list': current_list,
                    'tasks':current_list.tasks.all()
                }
                return render(request, 'tasks/list_page.html', context)
        
    
    
    current_list = ToDoList.objects.get(pk=list_id)
    tasks = current_list.tasks.order_by('time_start')
    context = {
        'list': current_list,
        'tasks':tasks
    }
    return render(request, 'tasks/list_page.html', context)

def change_background(request):
    if request.method == 'POST':
        user = request.user
        color = request.POST['color']
        user.background = color
        user.save()
        return render(request, 'tasks/change_background.html', {"message": 'Background changed!'})
    return render(request, 'tasks/change_background.html')
