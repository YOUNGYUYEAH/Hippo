# -*- encoding:utf-8 -*-
import json
from HippoWeb.Monitor import models
from HippoWeb.Monitor import MonitorORM
from django.shortcuts import HttpResponse, render
from django.contrib.auth.decorators import login_required


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
        return render(req, 'monitor/serverlist.html', {'data': _serverdata})
    except Exception as error:
        return render(req, 'monitor/serverlist.html', {'error': error})


def monitor_cpu(req):
    """
    查询所有服务CPU信息的接口,提供数值和百分比.
    """
    if req.is_ajax():
        if req.method == 'POST':
            if req.POST.get('option'):
                option = req.POST.get('option')
                title = "CPU List"
                thead = ["IP", "Load(1min)", "Load(5min)", "Load(15min)", "Count", "User", "System", "Nice",
                         "Idle", "IOwait", "Irq", "Softirq", "Steal", "Total", "Checktime"]
                try:
                    # 初始化前端页面所需要的数据.
                    s = MonitorORM.LoadData()
                    if option == "percent":
                        thead.pop(-2)
                        cpudata = s.load_cpu(percent=True)
                    else:
                        cpudata = s.load_cpu(percent=False)
                    response = HttpResponse(json.dumps({'title': title, 'head': thead, 'value': cpudata}),
                                            content_type='application/json')
                    return response
                except Exception as error:
                    # 如果有异常,将报错返回前端.
                    thead = ["Error Messages",]
                    response = HttpResponse(json.dumps({'title': title, 'head': thead, 'value': error}),
                                            content_type='application/json')
                    response.status_code = 417
                    return response
    else:
        # 仅接受AJAX.
        response = HttpResponse("ONLY AJAX. :(  \n")
        response.status_code = 405
        return response


def monitor_memory(req):
    """
    查询所有服务Memeory信息的接口,提供GB和MB单位.
    """
    if req.is_ajax():
        if req.method == 'POST':
            if req.POST.get('option'):
                unit = req.POST.get('option')
                title = "Memory List"
                thead = ["IP", "Total", "Available", "Used", "Free", "Active", "Inactive", "Buffers",
                         "Cached", "Shared", "Slab", "Checktime"]
                try:
                    s = MonitorORM.LoadData()
                    _data = s.load_memory()
                    memorydata = []
                    if _data:
                        for ip in _data:
                            _ipdata = []
                            for value in ip:
                                if isinstance(value, int):
                                    if unit == "MB":
                                        value = round(value/pow(1024, 2), 2)
                                    elif unit == "GB":
                                        value = round(value/pow(1024, 3), 2)
                                _ipdata.append(value)
                            memorydata.append(_ipdata)
                    response = HttpResponse(json.dumps({'title': title, 'head': thead, 'value': memorydata}),
                                            content_type='application/json')
                    return response
                except Exception as error:
                    thead = ["Error Messages",]
                    response = HttpResponse(json.dumps({'title': title, 'head': thead, 'value': error}),
                                            content_type='application/json')
                    response.status_code = 417
                    return response
    else:
        # 仅接受AJAX.
        response = HttpResponse("ONLY AJAX. :(  \n")
        response.status_code = 405
        return response


def monitor_disk(req):
    """
    查询所有服务磁盘用量信息的接口.
    """
    if req.is_ajax():
        if req.method == 'POST':
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
                response = HttpResponse(json.dumps({'title': title, 'head': thead, 'value': diskdata}),
                                        content_type='application/json')
                return response
            except Exception as error:
                print(error)
    else:
        # 仅接受AJAX.
        response = HttpResponse("ONLY AJAX. :(  \n")
        response.status_code = 405
        return response


def monitor_network(req):
    """
    查询服务器网卡接口信息
    """
    title = "Network List"
    thead = ["IP", "Interface", "Netaddr", "Speed", "pps[1s] sent/recv",
             "bps[1s] sent/recv", "Err in/out", "Checktime"]
    try:
        s = MonitorORM.LoadData()
        _data = s.load_network()
        networkdata = []
        for _ip in _data:
            arr = _ip[2].replace("'", '')
            ipvalue = [_ip[0], _ip[1][1:-1].split(","), arr, _ip[3]]
            networkdata.append(ipvalue)
        response = HttpResponse(json.dumps({'title': title, 'head': thead, 'value': networkdata}),
                                content_type='application/json')
        return response
    except Exception as error:
        return render(req, 'monitor/network.html', {'error': error})


@login_required
def monitordata(req):
    """
    根据选择返回监控数据,HostMode
    """
    try:
        return render(req, 'monitor/monitordata.html')
    except Exception as error:
        return render(req, 'monitor/monitordata.html', {'error': error})


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
