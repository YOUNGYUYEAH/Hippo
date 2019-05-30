from django import forms
import datetime
from HippoWeb.Monitor import models


class LoginForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'id': 'username', 'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'id': 'password', 'placeholder': 'Password', 'class': 'form-control'}))


class HostModeForm(forms.Form):
    ip = forms.ChoiceField(label='', widget=forms.Select(
        attrs={'id': 'select_ip', 'class': 'form-control selectpicker show-tick', 'data-style': 'btn-outline-primary',
               'autocomplete': 'off', 'data-live-search': 'true', 'data-width': '20%'}))
    charttype = forms.ChoiceField(label='', widget=forms.Select(
        attrs={'id': 'select_type', 'class': 'form-control selectpicker show-tick', 'data-style': 'btn-outline-primary',
               'autocomplete': 'off', 'data-width': '6%'}))
    timerange = forms.CharField(label='', widget=forms.DateTimeInput(
        attrs={'id': 'select_time', 'class': 'form-control', 'data-style': 'btn-outline-primary', 'text-align': 'center',
               'autocomplete': 'off', 'data-width': '350px',  'disabled': 'disabled'}))

    def __init__(self, *args, **kwargs):
        _server_list = []
        _load_server_result = models.Info.objects.all().values('id', 'ip', 'host')
        for i in _load_server_result:
            _server = [i["id"], "(" + i["ip"] + ") " + i["host"]]
            _server_list.append(_server)
        _count_result = models.Info.objects.all().count()

        type_list = ["CPU", "Disk", "Memory", "Network", "TCP", "ALL"]
        _type_list = []
        _count = 0
        for i in type_list:
            _count += 1
            _type_list.append([i.lower(), i])

        _nowtime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        _hoursago = str((datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
        _value = _hoursago + " — " + _nowtime

        super(HostModeForm, self).__init__(*args, **kwargs)
        self.fields['ip'].choices = _server_list
        self.fields['ip'].initial = _count_result
        self.fields['charttype'].choices = _type_list
        self.fields['charttype'].initial = _count
        self.fields['timerange'].widget.attrs.update({'value': _value})


class DateTimeForm(forms.Form):
    old_hours = forms.CharField(label='', max_length=2, widget=forms.NumberInput(
        attrs={'id': 'time_hours', 'class': 'form-control', 'min': '00', 'max': '23', 'step': '1',
               'style': 'width:40px; margin-left:18px;color:#000;'}))
    hours = forms.CharField(label='', max_length=2, widget=forms.NumberInput(
        attrs={'id': 'time_hours', 'class': 'form-control', 'min': '00', 'max': '23', 'step': '1',
               'style': 'width:40px; margin-left:18px;color:#000;'}))
    minutes = forms.CharField(label='', max_length=2, widget=forms.NumberInput(
        attrs={'id': 'time_minutes', 'class': 'form-control', 'min': '00', 'max': '59', 'step': '1',
               'style': 'width:40px; margin-left:18px;color:#000;'}))

    def __init__(self, *args, **kwargs):
        super(DateTimeForm, self).__init__(*args, **kwargs)
        _hours = str(datetime.datetime.now().strftime("%H"))
        _minutes = str(datetime.datetime.now().strftime("%M"))
        _old_hours = str((datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%H"))
        self.fields['hours'].widget.attrs.update({'value': _hours})
        self.fields['minutes'].widget.attrs.update({'value': _minutes})
        self.fields['old_hours'].widget.attrs.update({'value': _old_hours})
