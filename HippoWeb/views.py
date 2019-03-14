from django.conf import settings
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import auth
from HippoWeb.forms import *
import rsa

def login(req):
    """
    登录验证页
    """
    (pub_key, priv_key) = rsa.newkeys(512)
    pubkey_e = hex(pub_key.e)
    pubkey_n = hex(pub_key.n)
    if req.method == 'GET':
        login_form = LoginForm()
        return render(req, 'login.html', {'login_form': login_form, 'pubkey_e': pubkey_e, 'pubkey_n': pubkey_n})
    elif req.method == 'POST':
        username = req.POST.get('username', None)
        password = req.POST.get('password', None)
        return render(req, 'index.html', {'username': username, 'password': password})


def index(req):
    """
    主页,判断用户是否已经登录,若未登录则跳转login页
    """
    if req.method == 'POST':
        return render(req, 'index.html')
    else:
        return HttpResponseRedirect('/login/')
