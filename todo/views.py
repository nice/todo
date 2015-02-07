from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from todo.forms import UserLoginForm, UserRegisterForm

def user_login(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserLoginForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                user = cleaned_data.get('user')
                login(request, user)
                return HttpResponseRedirect('/')
        else:
            form = UserLoginForm()
        
        context = {
            'form': form,
        }
        context.update(csrf(request))
        return render(request, 'todo/templates/login.html', context)
    else:
        return HttpResponseRedirect('/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_register(request):
    context = {}
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Registration successfull. Please login.')
                return HttpResponseRedirect('/')
            else:
                context.update(csrf(request))
                context['form'] = form
                return render(request, 'todo/templates/register.html', context)
        else:
            form = UserRegisterForm()
        context.update(csrf(request))
        context['form'] = form
        return render(request, 'todo/templates/register.html', context)
    else:
        return HttpResponseRedirect('/')
