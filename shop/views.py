from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# Create your views here.

def user_login(request):
    return render(request, "user_login.html")

def page_login(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect('/admin')
                else:
                    return HttpResponseRedirect('/')
    

def homepage(request):
    return render(request, "homepage.html")