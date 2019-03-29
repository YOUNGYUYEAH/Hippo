# -*- encoding:utf-8 -*-
import json
from django.shortcuts import HttpResponse


def minitorjson(req):
    if req.method == 'GET':
        return HttpResponse("API error(405).")
    elif req.method == 'POST':
        if req.body:
            try:
                monitorjson = json.loads(req.body, encoding='utf-8')

                #return HttpResponse(monitorjson)
            except Exception as e:
                print(e)
                return HttpResponse("Bad Requests.")
        else:
            return HttpResponse("Empty Requests.")