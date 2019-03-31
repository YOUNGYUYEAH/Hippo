# -*- encoding:utf-8 -*-
from monitor import models


class Saveinfo(object):
    def __init__(self, monitorjson):
        self.system = monitorjson["system"]
        self.cpu = monitorjson["cpu"]
        self.memory = monitorjson["memory"]
        self.disk = monitorjson["disk"]
        self.network = monitorjson["network"]

    def save_cpu(self):
        models.cpu.objects.create(
            ip=self.system["ip"],
            loadavg=self.cpu["loadavg"],
            count=self.cpu["count"],
            user=self.cpu["user"],
            system=self.cpu["system"],
            nice=self.cpu["nice"],
            idle=self.cpu["idle"],
            iowait=self.cpu["iowait"],
            irq=self.cpu["irq"],
            softirq=self.cpu["softirq"],
            steal=self.cpu["steal"]
        )
