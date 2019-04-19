# -*- encoding:utf-8 -*-
from HippoWeb.monitor import models
from time import time, localtime, strftime
import json


class Saveinfo(object):
    """将Hippoagent传回来的monitorjson存入自定义的models表"""
    def __init__(self, monitorjson):
        self.system = monitorjson['system']
        self.cpu = monitorjson['cpu']
        self.memory = monitorjson['memory']
        self.disk = monitorjson['disk']
        self.network = monitorjson['network']
        self.checktime = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))

    def save_cpu(self):
        models.cpu.objects.create(
            ip=self.system['ip'],
            loadavg=self.cpu['loadavg'],
            user=self.cpu['user'],
            count=float(self.cpu['count']),
            system=float(self.cpu['system']),
            nice=float(self.cpu['nice']),
            idle=float(self.cpu['idle']),
            iowait=float(self.cpu['iowait']),
            irq=float(self.cpu['irq']),
            softirq=float(self.cpu['softirq']),
            steal=float(self.cpu['steal']),
            checktime=self.checktime
        )

    def save_memory(self):
        models.memory.objects.create(
            ip=self.system['ip'],
            total=int(self.memory['total']),
            available=int(self.memory['available']),
            used=int(self.memory['used']),
            free=int(self.memory['free']),
            active=int(self.memory['active']),
            inactive=int(self.memory['inactive']),
            buffers=int(self.memory['buffers']),
            cached=int(self.memory['cached']),
            shared=int(self.memory['shared']),
            slab=int(self.memory['slab']),
            checktime=self.checktime
        )

    def save_disk(self):
        models.disk.objects.create(
            ip=self.system["ip"],
            diskusage=json.dumps(self.disk["usage"]),
            iousage=json.dumps(self.disk["io"]),
            checktime=self.checktime
        )

    def save_network(self):
        models.network.objects.create(
            ip=self.system['ip'],
            network=json.dumps(self.network),
            checktime=self.checktime
        )

    def save_all(self):
        self.save_cpu()
        self.save_memory()
        self.save_disk()
        self.save_network()


class Loadinfo(object):
    """根据提交回来的ip进行数据库查询"""
    def __init__(self, ip=None, timerange=None, item=None):
        self.ip = ip
        self.timerange = timerange
        self.options = item
        self.count = models.info.objects.all().count()

    def load_info(self):
        """ORM提取回来的时间格式非正常显示,需要进一步处理"""
        if self.ip is not None:
            _load_info_result = models.info.objects.filter(ip=self.ip).\
                extra(select={'ctime': "DATE_FORMAT(create_time,'%%Y-%%m-%%d')",
                              'utime': "DATE_FORMAT(update_time,'%%Y-%%m-%%d')"}).\
                values('host', 'ip', 'platform', 'type', 'kernel', 'arch', 'ctime', 'utime', 'status', 'remark')
            return _load_info_result
        elif self.ip is None:
            _load_info_result = models.info.objects.all().\
                extra(select={'ctime': "DATE_FORMAT(create_time,'%%Y-%%m-%%d')",
                              'utime': "DATE_FORMAT(update_time,'%%Y-%%m-%%d')"}). \
                values('host', 'ip', 'platform', 'type', 'kernel', 'arch', 'ctime', 'utime', 'status', 'remark')
            return _load_info_result

