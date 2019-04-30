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
                        period=monitorjson_system['period']
                    )
                    s = MonitorORM.SaveData(monitorjson)
                    s.save_all()
                    response = HttpResponse()
                    response.status_code = 200
                    return response
            except Exception as e:
                return HttpResponse("Bad Requests.", {'error': e})
        else:
            return HttpResponse("Empty Requests.")


def serverlist(req):
    """
    返回所有info服务器的基本信息
    """
    s = MonitorORM.LoadData()
    serverinfo = s.load_info()
    return render(req, 'monitor/serverlist.html', {'data': serverinfo})


def monitor_cpu(req):
    s = MonitorORM.LoadData()
    cpudata = s.load_cpu()
    return render(req, 'monitor/cpu.html', {'data': cpudata})


def monitor_disk(req):
    s = MonitorORM.LoadData()
    diskdata = s.load_disk()
    for i in diskdata:
        print(i[0])
    return render(req, 'monitor/disk.html', {'diskdata': diskdata})


def monitor_memory(req):
    s = MonitorORM.LoadData()
    memorydata = s.load_memory()
    return render(req, 'monitor/memory.html', {'data': memorydata})


def monitor_network(req):
    s = MonitorORM.LoadData()
    networkdata = s.load_network()
    return render(req, 'monitor/network.html', {'data': networkdata})


def monitordata(req):
    """
    根据选择返回监控数据,HostMode
    """
    if req.method == 'GET':
        # 根据前端传递的参,调取不同的方法,然后将数据范围给前端页面
        try:
            s = MonitorORM.LoadData()
            memorydata = s.load_memory()
            diskdata = s.load_disk()
            return render(req, 'monitor/monitordata.html')
        except Exception as e:
            print(e)
