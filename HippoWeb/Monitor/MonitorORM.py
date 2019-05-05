# -*- encoding:utf-8 -*-
from django.db import connection
from time import time, localtime, strftime
from HippoWeb.Monitor import models
import json


class SaveData(object):
    """将Hippoagent传回来的monitorjson存入自定义的models表"""
    def __init__(self, monitorjson):
        self.system = monitorjson['system']
        self.cpu = monitorjson['cpu']
        self.memory = monitorjson['memory']
        self.disk = monitorjson['disk']
        self.network = monitorjson['network']
        self.option = monitorjson['period']
        self.checktime = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))

    def save_cpu(self):
        models.Cpu.objects.create(
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
        models.Memory.objects.create(
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
        models.Disk.objects.create(
            ip=self.system["ip"],
            diskusage=json.dumps(self.disk["usage"]),
            iousage=json.dumps(self.disk["io"]),
            checktime=self.checktime
        )

    def save_network(self):
        models.Network.objects.create(
            ip=self.system['ip'],
            network=json.dumps(self.network),
            checktime=self.checktime
        )

    def save_all(self):
        self.save_cpu()
        self.save_memory()
        self.save_disk()
        self.save_network()


class LoadData(object):
    """根据提交回来的ip进行数据库查询"""
    def __init__(self, ip=None, timerange=None, item=None):
        self.ip = ip
        self.timerange = timerange
        self.options = item
        # self.count = models.Info.objects.all().count()

    def load_info(self):
        """ORM提取回来的时间格式非正常显示,需要进一步处理"""
        if self.ip is not None:
            _load_info_result = models.Info.objects.filter(ip=self.ip).\
                extra(select={'ctime': "DATE_FORMAT(create_time,'%%Y-%%m-%%d')",
                              'utime': "DATE_FORMAT(update_time,'%%Y-%%m-%%d')"}).\
                values('host', 'ip', 'platform', 'type', 'kernel', 'arch', 'ctime', 'utime', 'status', 'remark')
            return _load_info_result
        elif self.ip is None:
            _load_info_result = models.Info.objects.all().\
                extra(select={'ctime': "DATE_FORMAT(create_time,'%%Y-%%m-%%d')",
                              'utime': "DATE_FORMAT(update_time,'%%Y-%%m-%%d')"}). \
                values('host', 'ip', 'platform', 'type', 'kernel', 'arch', 'ctime', 'utime', 'status', 'remark')
            return _load_info_result

    def load_cpu(self):
        """读取CPU信息需做差值处理和百分比计算"""
        if self.ip is not None:
            pass
        elif self.ip is None:
            pass

    def load_disk(self):
        """读取磁盘信息,磁盘信息需要进行JSON串处理"""
        try:
            cursor = connection.cursor()
            if self.ip is None:
                _querysql = """SELECT `ip`,`diskusage`,`iousage`,DATE_FORMAT(`checktime`,'%Y-%m-%d %H:%i:%S') 
                FROM monitor_disk WHERE `checktime` IN (SELECT Max(`checktime`) FROM monitor_disk GROUP BY `ip`);"""
                cursor.execute(_querysql)
                _load_disk_result = cursor.fetchall()
                return _load_disk_result
            else:
                _querysql = """SELECT `ip`,`diskusage`,`iousage`,DATE_FORMAT(Max(`checktime`),'%%Y-%%m-%%d %%H:%%i:%%S') 
                FROM monitor_disk WHERE `ip` = '%s';""" % self.ip
                cursor.execute(_querysql)
                _load_disk_result = cursor.fetchall()
                return _load_disk_result
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def load_disk_range(self):
        """读取时间范围内的磁盘信息"""
        pass

    def load_memory(self):
        """读取内存信息需进行单位换算,使用原生SQL,注意由于%和%%使用的不同"""
        try:
            cursor = connection.cursor()
            if self.ip is None:
                _querysql = """SELECT `ip`,`total`,`available`,`used`,`free`,`active`,`inactive`,`buffers`,`cached`,
                `shared`,`slab`,DATE_FORMAT(`checktime`,'%Y-%m-%d %H:%i:%S') FROM monitor_memory WHERE `checktime` 
                IN (SELECT Max(`checktime`) FROM monitor_memory GROUP BY `ip`);"""
                cursor.execute(_querysql)
                _load_memory_result = cursor.fetchall()
                return _load_memory_result
            else:
                _querysql = """SELECT `ip`,`total`,`available`,`used`,`free`,`active`,`inactive`,`buffers`,`cached`,
                `shared`,`slab`,DATE_FORMAT(Max(`checktime`),'%%Y-%%m-%%d %%H:%%i:%%S') FROM monitor_memory WHERE 
                `ip` = '%s';""" % self.ip
                cursor.execute(_querysql)
                _load_memory_result = cursor.fetchall()
                return _load_memory_result
        except Exception as e:
            print(e)
        finally:
            cursor.close()

    def load_memory_range(self):
        """读取时间范围内的内存信息"""
        pass

    def load_network(self):
        pass