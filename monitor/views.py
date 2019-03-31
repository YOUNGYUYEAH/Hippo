# -*- encoding:utf-8 -*-
import json
from monitor import models
from django.shortcuts import HttpResponse
from monitor.save_monitorinfo import Saveinfo


def minitorjson(req):
    if req.method == 'GET':
        return HttpResponse("API error(405).")
    elif req.method == 'POST':
        if req.body:
            try:
                monitorjson = json.loads(req.body, encoding='utf-8')
                monitorjson_system = monitorjson["system"]
                if models.info.objects.filter(ip=monitorjson_system["ip"]):
                    Saveinfo(monitorjson)
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
                    Saveinfo(monitorjson)
                    response = HttpResponse()
                    response.status_code = 200
                    return response
            except Exception as e:
                return HttpResponse("Bad Requests.", {"error": e})
        else:
            return HttpResponse("Empty Requests.")
