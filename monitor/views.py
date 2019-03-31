# -*- encoding:utf-8 -*-
import json
from monitor import models
from save_info import Saveinfo
from django.shortcuts import HttpResponse



def minitorjson(req):
    if req.method == 'GET':
        return HttpResponse("API error(405).")
    elif req.method == 'POST':
        if req.body:
            try:
                monitorjson = json.loads(req.body, encoding='utf-8')
                monitorjson_system = monitorjson["system"]
                if models.info.objects.filter(ip=monitorjson_system["ip"]):
                    s = save_monitorinfo.Saveinfo(monitorjson)
                    s.save_cpu()
                    response = HttpResponse()
                    response.status_code = 200
                    return response
                else:
                    models.info.objects.create(
                        host=monitorjson_system["hostname"],
                        ip=monitorjson_system["ip"],
                        platform=monitorjson_system["platform"],
                        type=monitorjson_system["type"],
                        kernel=monitorjson_system["kernel"],
                        arch=monitorjson_system["arch"],
                    )
                    s = save_monitorinfo.Saveinfo(monitorjson)
                    s.save_cpu()
                    response = HttpResponse()
                    response.status_code = 200
                    return response
            except Exception as e:
                return HttpResponse("Bad Requests.", {"error": e})
        else:
            return HttpResponse("Empty Requests.")
