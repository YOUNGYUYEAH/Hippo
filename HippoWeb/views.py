from django.shortcuts import render
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
        return render(req, 'index.html', {'username': username, 'password': password})