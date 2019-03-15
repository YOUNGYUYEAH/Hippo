from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect
from django.contrib import auth
from HippoWeb.forms import *
import rsa


def rsa_encrypt(req):
    """使用RSA生成公钥私钥"""
    (public, private) = rsa.newkeys(512)
    req.session['privkey'] = str(private)  # session存放在 django_session表内
    pubkey = {'pub_e': hex(public.e), 'pub_n': hex(public.n)}  # hex转化为16进制数
    return pubkey

def login(req):
    """登录验证页"""
    pubkey = rsa_encrypt(req)
    pub_e = pubkey['pub_e']
    pub_n = pubkey['pub_n']
    login_user = req.COOKIES.get('username')
    if login_user:
        return HttpResponseRedirect('/index/')
    else:
        login_form = LoginForm()
        if req.method == 'GET':
            return render_to_response('login.html', {'login_form': login_form, 'pub_e': pub_e, 'pub_n': pub_n})
        elif req.method == 'POST':
            username = req.POST.get('username', None)
            password = req.POST.get('password', None)
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                req.session['IS_LOGIN'] = True
                auth.login(req, user)
                response = render_to_response('index.html', {'username': username})
                response.set_cookie('username', username)
                return response
            else:
                return render(req, 'login.html', {'login_form': login_form, 'password_wrong': True, 'pub_e': pub_e, 'pub_n': pub_n})


def logout(req):
    """注销已登录用户"""
    login_user = req.COOKIES.get('username')
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
