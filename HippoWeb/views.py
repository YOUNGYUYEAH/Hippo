from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import auth
from HippoWeb.forms import *
import rsa

def login(req):
    """登录验证页"""
    login_user = req.COOKIES.get('username')
    if login_user:
        return HttpResponseRedirect('/index/')
    else:
        login_form = LoginForm()
        if req.method == 'GET':
            return render(req, 'login.html', {'login_form': login_form})
        elif req.method == 'POST':
            username = req.POST.get('username', None)
            password = req.POST.get('password', None)
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                req.session['IS_LGOIN'] = True
                response = redirect('/index/')
                response.set_cookie('username', username)
                auth.login(req, user)
                return response
            else:
                return render(req, 'login.html', {'login_form': login_form, 'passwd_wrong': True})


def logout(req):
    """注销已登录用户"""
    login_user =  req.COOKIES.get('username')
    if login_user:
        response = redirect('/login/')
        response.delete_cookie('username')
        auth.logout(req)
        return response
    else:
        return HttpResponseRedirect('/login/')


def index(req):
    """主页,判断用户是否已经登录,若未登录则跳转login页"""
    login_user = req.COOKIES.get('username')
    if login_user:
        return render(req, 'index.html', {'login_user': login_user})
    else:
        return HttpResponseRedirect('/login/')
