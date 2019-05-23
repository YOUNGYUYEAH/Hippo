from django import forms
from django.forms import widgets
from HippoWeb.Monitor import models
from HippoWeb.Monitor import MonitorORM


class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'id': 'username', 'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'id': 'password', 'placeholder': 'Password', 'class': 'form-control'}))


class HostModeForm(forms.Form):
    _server_list = []
    _load_server_result = models.Info.objects.all().values('id', 'ip', 'host')
    for i in _load_server_result:
        _server = [i["id"], "(" + i["ip"] + ") " + i["host"]]
        _server_list.append(_server)
    _count_result = models.Info.objects.all().count()
    try:
        ip = forms.ChoiceField(label='', choices=_server_list,  widget=forms.Select(
            attrs={'id': 'select_host_ip', 'class': 'form-control selectpicker show-tick', 'data-style': 'btn-default',
                   'autocomplete': 'off', 'data-live-search': 'true', 'data-width': '20%'}), initial=_count_result)
    except Exception as error:
        ip = forms.ChoiceField(label='', choices=("", error), widget=forms.Select(
            attrs={'id': 'select_host_ip', 'class': 'form-control selectpicker show-tick', 'data-style': 'btn-default',
                   'autocomplete': 'off', 'data-live-search': 'true', 'data-width': '20%'}), initial=1)
