import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import serializers

from website.forms import NewTaskForm
from website.models import Task

@login_required
def index(request):
    context = {}
    # fetching recent tasks
    tasks = Task.objects.filter(user=request.user).order_by('priority')
    context = {
        'tasks': tasks,
        'form': NewTaskForm()
    }
    context.update(csrf(request))
    return render(request, 'website/templates/index.html', context)

@login_required
def new_task(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.priority = 3
            data.state = 'todo'
            data.save()
            messages.success(request, 'Task added successfully.')
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
    if request.method == 'POST':
        id = request.POST.get('id')
        task = Task.objects.get(pk=id)
        if task.user == request.user:
            data = serializers.serialize('json', [ task, ])
            struct = json.loads(data)
            data = json.dumps(struct[0])
            return JsonResponse(data, safe=False)
    else:
        return HttpResponseRedirect('/')
