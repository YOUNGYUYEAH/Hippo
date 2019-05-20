from django import forms
from django.forms import widgets
from HippoWeb.Monitor import MonitorORM


class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'id': 'username', 'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'id': 'password', 'placeholder': 'Password', 'class': 'form-control'}))


class HostModeForm(forms.Form):
    s = MonitorORM.LoadData()
    try:
        ip = forms.ChoiceField(label='', choices=s.load_server(),  widget=forms.Select(
            attrs={'id': 'select_host_ip', 'class': 'form-control selectpicker',
                   'data-live-search': 'true', 'data-width': '25%'}), initial=s.count())
    except Exception as error:
        ip = forms.ChoiceField(label='', choices=("", error), widgets=forms.Select(
            attrs={'id': 'select_host_ip', 'class': 'form-control selectpicker show-tick',
                   'data-live-search': 'true', 'data-width': '25%'}), initial=1)
