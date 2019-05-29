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
        attrs={'id': 'select_ip', 'class': 'form-control selectpicker show-tick', 'data-style': 'btn-default',
               'autocomplete': 'off', 'data-live-search': 'true', 'data-width': '20%'}))

    def __init__(self, *args, **kwargs):
        _server_list = []
        _load_server_result = models.Info.objects.all().values('id', 'ip', 'host')
        for i in _load_server_result:
            _server = [i["id"], "(" + i["ip"] + ") " + i["host"]]
            _server_list.append(_server)
        _count_result = models.Info.objects.all().count()
        super(HostModeForm, self).__init__(*args, **kwargs)
        self.fields['ip'].choices = _server_list
        self.fields['ip'].initial = _count_result


class ChartTypeForm(forms.Form):
    type_list = ["CPU", "Disk", "Memory", "Network", "TCP", "ALL"]
    _type_list = []
    _count = 0
    for i in type_list:
        _count += 1
        _type_list.append([i.lower(), i])
    charttype = forms.ChoiceField(label='', choices=_type_list, widget=forms.Select(
        attrs={'id': 'select_chart_type', 'class': 'form-control selectpicker show-tick', 'data-style': 'btn-default',
               'autocomplete': 'off', 'data-width': '6%'}), initial=_count)


class TimePickerForm(forms.Form):
    timerange = forms.DateTimeField(label='', widget=forms.TextInput(
        attrs={'id': 'select_time', 'class': 'form-control selectpicker', 'data-style': 'btn-default',
               'style': 'width: 88%; float:left;', 'disabled': 'disabled'}))

    def __init__(self, *args, **kwargs):
        _nowtime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        _hoursago = str((datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
        _value = _hoursago + " — " + _nowtime
        super(TimePickerForm, self).__init__(*args, **kwargs)
        self.fields['timerange'].widget.attrs.update({'value': _value})
