# -*- encoding:utf-8 -*-
import json
from HippoWeb.Monitor import models
from HippoWeb.Monitor import MonitorORM
from django.shortcuts import HttpResponse, render
from django.contrib.auth.decorators import login_required
from HippoWeb.forms import HostModeForm


def collect(req):
    """
    接收agent数据的接口,仅接收方法为POST的请求,将数据判断后入库.
    """
    if req.method == 'POST':
        if req.body:
            try:
                monitorjson = json.loads(req.body, encoding='utf-8')
                monitorjson_system = monitorjson['system']
                if models.Info.objects.filter(ip=monitorjson_system['ip']):
                    # 需要判断新的数据是否跟源数据不同,若不同需要更新.
                    s = MonitorORM.SaveData(monitorjson)
                    s.save_all()
                    response = HttpResponse()
                    response.status_code = 200
                    return response
                else:
                    # 若不存在对应IP数据,则进行添加,顺便存入数据,返回API正常.
                    models.Info.objects.create(
                        host=monitorjson_system['hostname'],
                        ip=monitorjson_system['ip'],
                        platform=monitorjson_system['platform'],
                        type=monitorjson_system['type'],
                        kernel=monitorjson_system['kernel'],
                        arch=monitorjson_system['arch'],
                    )
                    s = MonitorORM.SaveData(monitorjson)
                    s.save_all()
                    response = HttpResponse()
                    response.status_code = 200
                    return response
            except Exception as error:
                # 请求异常,需要补充记录日志.
                print(error)
                response = HttpResponse("Bad Requests. \n")
                response.status_code = 412
                return response
        else:
            # 无任何请求报错.
            response = HttpResponse("Empty Request. =.=? \n")
            response.status_code = 412
            return response
    else:
        # 非POST方法报错.
        response = HttpResponse("API Error. :(  \n")
        response.status_code = 405
        return response


@login_required
def serverlist(req):
    """
    读取monitor_info返回所有服务器的基本信息.
    """
    try:
        s = MonitorORM.LoadData()
        _serverdata = s.load_info()
    except Exception as error:
        _serverdata = error
    return render(req, 'monitor/serverlist.html', {'data': _serverdata})


def monitor_host(option):
    """前端返回需要搜索的服务器的id,通过id获取ip,然后获取值"""
    pass


def monitor_cpu(option):
    """
    查询所有服务CPU信息的接口,提供数值和百分比.
    """
    title = "CPU List"
    thead = ["IP", "Load(1min)", "Load(5min)", "Load(15min)", "Count", "User", "System", "Nice","Idle", "IOwait",
             "Irq", "Softirq", "Steal", "Total", "Checktime"]
    try:
        s = MonitorORM.LoadData()
        if option == "percent":
            thead.pop(-2)
            cpudata = s.load_cpu(percent=True)
        else:
            cpudata = s.load_cpu(percent=False)
    except Exception as error:
        cpudata = error
    _response = HttpResponse(json.dumps({'title': title, 'head': thead, 'value': cpudata}),
                             content_type='application/json')
    return _response


def monitor_memory(option):
    """
    查询所有服务Memeory信息的接口,提供GB和MB单位.
    """
    title = "Memory List"
    thead = ["IP", "Total", "Available", "Used", "Free", "Active", "Inactive", "Buffers", "Cached", "Shared",
             "Slab", "Checktime"]
    try:
        s = MonitorORM.LoadData()
        _data = s.load_memory()
        memorydata = []
        if _data:
            for ip in _data:
                _ipdata = []
                for value in ip:
                    if isinstance(value, int):
                        if option == "MB":
                            value = round(value/pow(1024, 2), 2)
                        elif option == "GB":
                            value = round(value/pow(1024, 3), 2)
                    _ipdata.append(value)
                memorydata.append(_ipdata)
    except Exception as error:
        memorydata = error
    _response = HttpResponse(json.dumps({'title': title, 'head': thead, 'value': memorydata}),
                             content_type='application/json')
    return _response


def monitor_disk():
    """
    查询所有服务磁盘用量信息的接口.
    """
    title = "Disk List"
    thead = ["IP", "Mount", "Usage", "Checktime"]
    try:
        s = MonitorORM.LoadData()
        _data = s.load_disk()
        diskdata = []
        for _ip in _data:
            arr = _ip[2].replace("'", '')
            ipvalue = [_ip[0], _ip[1][1:-1].split(","), arr, _ip[3]]
            diskdata.append(ipvalue)
    except Exception as error:
        diskdata = error
    _response = HttpResponse(json.dumps({'title': title, 'head': thead, 'value': diskdata}),
                             content_type='application/json')
    return _response


def monitor_network():
    """
    查询服务器网卡接口信息
    """
    title = "Network List"
    thead = ["IP", "Interface", "Netaddr", "Speed", "pps[1s] sent/recv", "bps[1s] sent/recv", "Err in/out", "Checktime"]
    try:
        s = MonitorORM.LoadData()
        _data = s.load_network()
        networkdata = []
        for _ip in _data:
            arr = _ip[2].replace("'", '')
            ipvalue = [_ip[0], _ip[1][1:-1].split(","), arr, _ip[3]]
            networkdata.append(ipvalue)
    except Exception as error:
        networkdata = error
    _response = HttpResponse(json.dumps({'title': title, 'head': thead, 'value': networkdata}),
                             content_type='application/json')
    return _response


@login_required
def monitordata(req):
    """
    根据选择返回监控数据,HostMode
    """
    try:
        hostmode_form = HostModeForm()
        return render(req, 'monitor/monitordata.html', {'hostmode_form': hostmode_form})
    except Exception as error:
        return render(req, 'monitor/monitordata.html', {'error': error})


def search(req):
    if req.is_ajax():
        if req.method == 'POST':
            search_type = req.POST.get('type')
            if search_type == "host":
                _option = req.POST.get('option')
                print(_option)
            elif search_type == "cpu":
                _option = req.POST.get('option')
                response = monitor_cpu(_option)
                return response
            elif search_type == "memory":
                _option = req.POST.get('option')
                response = monitor_memory(_option)
                return response
            elif search_type == "disk":
                _response = monitor_disk()
                return _response
            elif search_type == "network":
                _response = monitor_network()
                return _response
            else:
                pass
        else:
            # 非POST方法报错.
            response = HttpResponse("API Error. :(  \n")
            response.status_code = 405
            return response
    else:
        # 仅接受AJAX.
        response = HttpResponse("ONLY AJAX. :(  \n")
        response.status_code = 405
        return response


def addserver(req):
    """
    添加新的监控服务器,分配agent,需要通过saltstack分配安装
    """
    pass


def charts(req):
    """
    根据数据出图
    """
    pass
