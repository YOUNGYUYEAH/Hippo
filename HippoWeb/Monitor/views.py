# -*- encoding:utf-8 -*-
import json
from HippoWeb.Monitor import models
from HippoWeb.Monitor import MonitorORM
from django.shortcuts import HttpResponse, render


def collect(req):
    """
    接收agent数据的接口,仅接收方法为POST的请求,
    将数据判断后入库
    """
    if req.method == 'GET':
        return HttpResponse("API error(405).")
    elif req.method == 'POST':
        if req.body:
            try:
                monitorjson = json.loads(req.body, encoding='utf-8')
                monitorjson_system = monitorjson['system']
                if models.Info.objects.filter(ip=monitorjson_system['ip']):
                    # 需要判断新的数据是否跟源数据不同,若不同需要更新
                    s = MonitorORM.SaveData(monitorjson)
                    s.save_all()
                    response = HttpResponse()
                    response.status_code = 200
                    return response
                else:
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
                return HttpResponse("Bad Requests.", {'error': error})
        else:
            return HttpResponse("Empty Requests.")


def serverlist(req):
    """
    返回所有info服务器的基本信息
    """
    try:
        s = MonitorORM.LoadData()
        serverinfo = s.load_info()
        return render(req, 'monitor/serverlist.html', {'data': serverinfo})
    except Exception as error:
        return render(req, 'monitor/serverlist.html', {'error': error})


def monitor_cpu(req):
    value = False
    try:
        s = MonitorORM.LoadData()
        if value:
            cpudata = s.load_cpu(percent=None)
            return render(req, 'monitor/cpu.html', {'data': cpudata, 'value': value})
        else:
            cpudata = s.load_cpu(percent=True)
            return render(req, 'monitor/cpu.html', {'data': cpudata, 'value': value})
    except Exception as error:
        return render(req, 'monitor/cpu.html', {'error': error})


def monitor_disk(req):
    try:
        s = MonitorORM.LoadData()
        diskdata = s.load_disk()
        return render(req, 'monitor/disk.html', {'data': diskdata})
    except Exception as error:
        return render(req, 'monitor/disk.html', {'error': error})


def monitor_memory(req):
    """
    通过前端获取回来的option值,如果没有则默认值MB
    额外计算一个内存使用占百分比回显页面
    """
    try:
        if req.is_ajax():
            if req.GET.get('unit'):
                unit = req.GET.get('unit')
            elif req.POST.get('unit'):
                unit = req.POST.get('unit')
            else:
                unit = "GB"
        memorydata = []
        s = MonitorORM.LoadData()
        _data = s.load_memory()
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
        response = render(req, 'monitor/memory.html', {'data': memorydata, 'unit': unit})
        response.status_code = 200
        return response
    except Exception as error:
        return render(req, 'monitor/memory.html', {'error': error})


def monitor_network(req):
    try:
        s = MonitorORM.LoadData()
        networkdata = s.load_network()
        return render(req, 'monitor/network.html', {'data': networkdata})
    except Exception as error:
        return render(req, 'monitor/network.html', {'error': error})


def monitordata(req):
    """
    根据选择返回监控数据,HostMode
    """
    try:
        s = MonitorORM.LoadData()
        data = s
        return render(req, 'monitor/monitordata.html', {'data': s})
    except Exception as error:
        return render(req, 'monitor/monitordata.html', {'error': error})


def addserver(req):
    """添加新的监控服务器,分配agent,需要通过saltstack分配安装"""
    pass


def charts(req):
    """根据数据出图"""
    pass
