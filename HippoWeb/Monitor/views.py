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
                if models.info.objects.filter(ip=monitorjson_system['ip']):
                    # 需要判断新的数据是否跟源数据不同,若不同需要更新
                    s = MonitorORM.Saveinfo(monitorjson)
                    s.save_all()
                    response = HttpResponse()
                    response.status_code = 200
                    return response
                else:
                    models.info.objects.create(
                        host=monitorjson_system['hostname'],
                        ip=monitorjson_system['ip'],
                        platfMonitorORM=monitorjson_system['platfMonitorORM'],
                        type=monitorjson_system['type'],
                        kernel=monitorjson_system['kernel'],
                        arch=monitorjson_system['arch'],
                    )
                    s = MonitorORM.Saveinfo(monitorjson)
                    s.save_all()
                    response = HttpResponse()
                    response.status_code = 200
                    return response
            except Exception as e:
                return HttpResponse("Bad Requests.", {'error': e})
        else:
            return HttpResponse("Empty Requests.")


def monitor_alerm(req):
    pass


def monitor_info(req):
    # if req.method == 'GET':
    #    _i = monitorjson_MonitorORM.Loadinfo()
    if req.method == 'GET':
        # 获取前端传回的target_ip,若没有传回则默认读取全部,但分页展示
        try:
            _i = MonitorORM.Loadinfo()
            json_list = []
            for index in range(len(_i.load_info())):
                monitorjson = json.dumps(_i.load_info()[index])
                json_list.append(monitorjson)
            web_type = 'monitor_info'
            return render(req, 'index.html', {'web_type': web_type, 'msg': json_list})
        except Exception as e:
            print(e)