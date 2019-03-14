from django.shortcuts import render
from django.contrib import auth
from HippoWeb.forms import *

# Create your views here.

def login(req):
    """登录验证页"""
    if req.method == 'GET':
        login_form = LoginForm()
        return render(req, 'login.html', {'login_form': login_form})
    elif req.method == 'POST':
        login_form = LoginForm(req.POST)
        if login_form.is_valid():
            username = req.POST.get('username', '')
            password = req.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(req, user)
                return render(req, 'index.html', {'username': username, 'password': password})
            else:
                return render(req, 'index.html', {'username': username, 'password': password, 'is_wrong': True})
        else:
            return render(req, 'login.html', {'login_form': login_form})

