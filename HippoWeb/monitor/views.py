# -*- encoding:utf-8 -*-
import json
from HippoWeb.monitor import models
from HippoWeb.monitor import monitorjson_orm
from django.shortcuts import HttpResponse



def minitorjson(req):
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
                    s = monitorjson_orm.Saveinfo(monitorjson)
                    s.save_all()
                    response = HttpResponse()
                    response.status_code = 200
                    return response
                else:
                    models.info.objects.create(
                        host=monitorjson_system['hostname'],
                        ip=monitorjson_system['ip'],
                        platform=monitorjson_system['platform'],
                        type=monitorjson_system['type'],
                        kernel=monitorjson_system['kernel'],
                        arch=monitorjson_system['arch'],
                    )
                    s = monitorjson_orm.Saveinfo(monitorjson)
                    s.save_all()
                    response = HttpResponse()
                    response.status_code = 200
                    return response
            except Exception as e:
                return HttpResponse("Bad Requests.", {'error': e})
        else:
            return HttpResponse("Empty Requests.")
