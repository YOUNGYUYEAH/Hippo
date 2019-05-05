# -*- encoding:utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from HippoWeb.forms import *
import rsa
import json


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('50x.html')
    response.status_code = 500
    return response


def rsa_encrypt(req):
    """使用RSA生成公钥私钥,并拆分存放private key"""
    (public, private) = rsa.newkeys(512)
    private_key = {}
    private_key['n'] = private.n
    private_key['e'] = private.e
    private_key['d'] = private.d
    private_key['p'] = private.p
    private_key['q'] = private.q
    req.session['privkey'] = private_key          # session存放在 django_session表内
    pub_e = hex(public.e).split('0x')[1]          # hex转化为16进制数再截去0x头部
    pub_n = hex(public.n).split('0x')[1]
    # print(pub_e)
    # print(pub_n)
    pubkey = {'pub_e': pub_e, 'pub_n': pub_n}
    return pubkey


def rsa_privkey(req):
    """从session中提取private key"""
    priv = req.session.get('privkey')
    privkey = rsa.PrivateKey(priv['n'],
                             priv['e'],
                             priv['d'],
                             priv['p'],
                             priv['q'])
    return privkey


def login(req):
    """返回登录页表单"""
    login_user = req.COOKIES.get('username')
    if login_user:
        return redirect('/index/')
    pubkey = rsa_encrypt(req)
    pub_e = pubkey['pub_e']
    pub_n = pubkey['pub_n']
    login_form = LoginForm()
    return render(req, 'login.html', {'login_form': login_form, 'pub_e': pub_e, 'pub_n': pub_n})


def checklogin(req):
    """检验登录数据"""
    if req.is_ajax():
        if req.method == 'POST':
            username = req.POST.get('username', None)
            en_password = req.POST.get('en_password', None)
            if en_password:
                # RSA加密暂时搁置先不实现, MMP
                password = req.POST.get('password', None)
                # privkey = rsa_privkey(req)
                # py2使用en_password.decode('hex')
                # password = rsa.decrypt(bytes.fromhex(en_password), privkey)
                # req.session['privkey'] = None
                user = auth.authenticate(username=username, password=password)
                if user:
                    auth.login(req, user)
                    response = HttpResponse(json.dumps({'data': "ok"}))
                    response.set_cookie('username', user)
                    return response
                else:
                    response = HttpResponse(json.dumps({'data': "error"}))
                    return response
                # 添加账号密码判断反馈回前端


def logout(req):
    """注销已登录用户"""
    login_user = req.COOKIES.get('username')
    if login_user:
        response = redirect('/login/')
        response.delete_cookie('username')
        auth.logout(req)
        return response
    else:
        return redirect('/login/')


@login_required
def index(req):
    try:
        """主页,判断用户是否已经登录,若未登录则跳转login页"""
        login_user = req.COOKIES.get('username')
        if login_user:
            return render(req, 'index.html', {'login_user': login_user})
        else:
            return redirect('/login/')
    except Exception as error:
        print(error)
