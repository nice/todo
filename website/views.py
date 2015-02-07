import json
from datetime import date, datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers

from website.forms import TaskForm
from website.models import Task

@login_required
def index(request):
    context = {}
    # fetching recent tasks
    tasks = Task.objects.filter(user=request.user).order_by('priority')
    context = {
        'tasks': tasks,
        'form': TaskForm()
    }
    context.update(csrf(request))
    return render(request, 'website/templates/index.html', context)

@login_required
def task(request, task_id=None):
    if request.method == 'POST':
        if task_id:
            task = Task.objects.get(pk=task_id)
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                if task.user == request.user:
                    data = form.save(commit=False)
                    data.user = request.user
                    data.save()
                    messages.success(request, 'Task updated successfully.')
                    if 'next' in request.POST:
                        return HttpResponseRedirect(request.POST.get('next'))
                    return HttpResponseRedirect('/')
        else:
            # creating new task
            form = TaskForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.priority = 3
                data.state = 'todo'
                data.save()
                messages.success(request, 'Task added successfully.')
                if 'next' in request.POST:
                    return HttpResponseRedirect(request.POST.get('next'))
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def update_task(request, item):
    if request.method == 'POST':
        if item == 'priority':
            id = request.POST.get('id')
            priority = request.POST.get('priority')
            task = Task.objects.get(pk=id)
            if task.user == request.user:
                task.priority = priority
                task.save()
                return HttpResponse('saved')
        elif item == 'state':
            id = request.POST.get('id')
            state = request.POST.get('state')
            task = Task.objects.get(pk=id)
            if task.user == request.user:
                task.state = state
                task.save()
                return HttpResponse('saved')
    else:
        return HttpResponseRedirect('/')

# actions
@csrf_exempt
def view_task(request):
    context = {}
    id = request.GET.get('id')
    task = Task.objects.get(pk=id)
    if task.user == request.user:
        data = serializers.serialize('json', [ task, ])
        struct = json.loads(data)
        data = json.dumps(struct[0])
        return JsonResponse(data, safe=False)
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def delete_task(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        task = Task.objects.get(pk=id)
        if task.user == request.user:
            task.delete()
            messages.success(request, 'Task deleted successfully.')
    return HttpResponseRedirect('/')

# basic filtering
def filter(request, target='today'):
    context = {}
    if target == 'today':
        tasks = Task.objects.filter(user=request.user, due_date=date.today()).order_by('priority')
    elif target == 'week':
        tasks = Task.objects.filter(user=request.user, due_date__lte=datetime.now() + timedelta(days=7)).order_by('priority')
    elif target == 'month':
        tasks = Task.objects.filter(user=request.user, due_date__lte=datetime.now() + timedelta(days=30)).order_by('priority')
    elif target == 'expired':
        tasks = Task.objects.filter(user=request.user, due_date__lt=datetime.now()).order_by('priority')
    else:
        tasks = Task.objects.filter(user=request.user).order_by('priority')

    context = {
        'tasks': tasks,
        'form': TaskForm()
    }
    context.update(csrf(request))
    return render(request, 'website/templates/index.html', context)
