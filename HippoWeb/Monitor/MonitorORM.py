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
        self.checktime = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))

    def save_cpu(self):
        models.Cpu.objects.create(
            ip=self.system['ip'],
            load_1=self.cpu['load_1'],
            load_5=self.cpu['load_5'],
            load_15=self.cpu['load_15'],
            user=self.cpu['user'],
            count=float(self.cpu['count']),
            system=float(self.cpu['system']),
            nice=float(self.cpu['nice']),
            idle=float(self.cpu['idle']),
            iowait=float(self.cpu['iowait']),
            irq=float(self.cpu['irq']),
            softirq=float(self.cpu['softirq']),
            steal=float(self.cpu['steal']),
            total=float(self.cpu['total']),
            p_user=float(self.cpu['p_user']),
            p_nice=float(self.cpu['p_nice']),
            p_system=float(self.cpu['p_system']),
            p_idle=float(self.cpu['p_idle']),
            p_iowait=float(self.cpu['p_iowait']),
            p_irq=float(self.cpu['p_irq']),
            p_softirq=float(self.cpu['p_softirq']),
            p_steal=float(self.cpu['p_steal']),
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
            diskmount=self.disk["mount"],
            diskusage=self.disk["usage"],
            checktime=self.checktime
            )

    def save_network(self):
        models.Network.objects.create(
            ip=self.system['ip'],
            netpic=self.network["pernic"],
            netusage=self.network["usage"],
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
        self.cursor = connection.cursor()
        # self.count = models.Info.objects.all().count()

    def dictfetchall(self):
        columns = [col[0] for col in self.cursor.description]
        return [
            dict(zip(columns, row))
            for row in self.cursor.fetchall()
        ]

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

    def load_cpu(self, percent=True):
        try:
            if self.ip is None:
                if percent:
                    _query_percent_sql = """SELECT `ip`,`load_1`,`load_5`,`load_15`,`count`,`p_user`,`p_system`,`p_nice`,
                    `p_idle`,`p_iowait`,`p_irq`,`p_softirq`,`p_steal`,DATE_FORMAT(`checktime`,'%Y-%m-%d %H:%i:%S') 
                    FROM monitor_cpu WHERE `checktime` IN (SELECT Max(`checktime`) FROM monitor_cpu GROUP BY `ip`);"""
                    self.cursor.execute(_query_percent_sql)
                    _load_percent_result = self.cursor.fetchall()
                    return _load_percent_result
                else:
                    _query_value_sql = """SELECT `ip`,`load_1`,`load_5`,`load_15`,`count`,`user`,`system`,`nice`,`idle`,
                    `iowait`,`irq`,`softirq`,`steal`,`total`,DATE_FORMAT(`checktime`,'%Y-%m-%d %H:%i:%S') 
                    FROM monitor_cpu WHERE `checktime` IN (SELECT Max(`checktime`) FROM monitor_cpu GROUP BY `ip`);"""
                    self.cursor.execute(_query_value_sql)
                    _load_value_result = self.cursor.fetchall()
                    return _load_value_result
            else:
                if percent:
                    _query_percent_sql = """SELECT `ip`,`load_1`,`load_5`,`load_15`,`count`,`p_user`,`p_system`,`p_nice`,
                    `p_idle`,`p_iowait`,`p_irq`,`p_softirq`,`p_steal`,DATE_FORMAT(Max(`checktime`),'%%Y-%%m-%%d %%H:%%i:%%S')
                    FROM monitor_cpu WHERE `ip` = '%s';""" % self.ip
                    self.cursor.execute(_query_percent_sql)
                    _load_percent_result = self.cursor.fetchall()
                    return _load_percent_result
                else:
                    _query_value_sql = """SELECT `ip`,`load_1`,`load_5`,`load_15`,`count`,`user`,`system`,`nice`,`idle`,
                    `iowait`,`irq`,`softirq`,`steal`,`total`,DATE_FORMAT(Max(`checktime`),'%%Y-%%m-%%d %%H:%%i:%%S') 
                    FROM monitor_cpu WHERE `ip` = '%s';""" % self.ip
                    self.cursor.execute(_query_value_sql)
                    _load_value_result = self.cursor.fetchall()
                    return _load_value_result
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()

    def load_disk(self):
        """读取磁盘信息"""
        try:
            if self.ip is None:
                _querysql = """SELECT `ip`,`diskmount`,`diskusage`,DATE_FORMAT(`checktime`,'%Y-%m-%d %H:%i:%S') 
                AS `checktime` FROM monitor_disk WHERE `checktime` 
                IN (SELECT Max(`checktime`) FROM monitor_disk GROUP BY `ip`);"""
                self.cursor.execute(_querysql)
                _load_disk_result = self.cursor.fetchall()
                return _load_disk_result
            else:
                _querysql = """SELECT `ip`,`diskmount`,`diskusage`,DATE_FORMAT(Max(`checktime`) as `checktime`,
                '%%Y-%%m-%%d %%H:%%i:%%S') FROM monitor_disk WHERE `ip` = '%s';""" % self.ip
                self.cursor.execute(_querysql)
                _load_disk_result = self.cursor.fetchall()
                return _load_disk_result
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()

    def load_disk_range(self):
        """读取时间范围内的磁盘信息"""
        pass

    def load_memory(self):
        """读取内存信息需进行单位换算,使用原生SQL,注意由于%和%%使用的不同"""
        try:
            if self.ip is None:
                _querysql = """SELECT `ip`,`total`,`available`,`used`,`free`,`active`,`inactive`,`buffers`,`cached`,
                `shared`,`slab`,DATE_FORMAT(`checktime`,'%Y-%m-%d %H:%i:%S') FROM monitor_memory WHERE `checktime` 
                IN (SELECT Max(`checktime`) FROM monitor_memory GROUP BY `ip`);"""
                self.cursor.execute(_querysql)
                _load_memory_result = self.cursor.fetchall()
                return _load_memory_result
            else:
                _querysql = """SELECT `total`,`available`,`used`,`free`,`active`,`inactive`,`buffers`,`cached`,
                `shared`,`slab`,DATE_FORMAT(Max(`checktime`),'%%Y-%%m-%%d %%H:%%i:%%S') FROM monitor_memory WHERE 
                `ip` = '%s';""" % self.ip
                self.cursor.execute(_querysql)
                _load_memory_result = self.cursor.fetchall()
                return _load_memory_result
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()

    def load_memory_range(self):
        """读取时间范围内的内存信息"""
        pass

    def load_network(self):
        pass