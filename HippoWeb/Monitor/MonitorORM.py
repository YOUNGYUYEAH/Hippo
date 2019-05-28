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
            count=(self.cpu['count']),
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
    def __init__(self, ip=None, time_start=None, time_end=None):
        self.ip = ip
        self.ts = time_start
        self.te = time_end
        self.cursor = connection.cursor()

    def dictfetchall(self):
        columns = [col[0] for col in self.cursor.description]
        return [
            dict(zip(columns, row))
            for row in self.cursor.fetchall()
        ]

    def load_info(self):
        """ORM提取回来的时间格式非正常显示,需要进一步处理"""
        if self.ip:
            _load_info_result = models.Info.objects.filter(ip=self.ip).\
                extra(select={'createtime': "DATE_FORMAT(create_time,'%%Y-%%m-%%d')",
                              'updatetime': "DATE_FORMAT(update_time,'%%Y-%%m-%%d')"}).\
                values('host', 'ip', 'platform', 'type', 'kernel', 'arch', 'createtime', 'updatetime',
                       'status', 'remark')
            return _load_info_result[0]
        else:
            _load_info_result = models.Info.objects.all().\
                extra(select={'ctime': "DATE_FORMAT(create_time,'%%Y-%%m-%%d')",
                              'utime': "DATE_FORMAT(update_time,'%%Y-%%m-%%d')"}). \
                values('host', 'ip', 'platform', 'type', 'kernel', 'arch', 'ctime', 'utime', 'status', 'remark')
            return _load_info_result

    def load_cpu(self):
        try:
            if self.ip:
                _querysql = """SELECT `load_1`,`load_5`,`load_15`,`count`,`p_user`,`p_system`,`p_nice`,
                `p_idle`,`p_iowait`,`p_irq`,`p_softirq`,`p_steal`,DATE_FORMAT(`checktime`,'%%Y-%%m-%%d %%H:%%i:%%S') 
                AS `checktime` FROM monitor_cpu WHERE `checktime` IN (SELECT Max(`checktime`) FROM monitor_cpu 
                GROUP BY `ip`) AND `ip` = '%s';""" % self.ip
                self.cursor.execute(_querysql)
            else:
                _querysql = """SELECT `ip`,`load_1`,`load_5`,`load_15`,`count`,`p_user`,`p_system`,`p_nice`,
                `p_idle`,`p_iowait`,`p_irq`,`p_softirq`,`p_steal`,DATE_FORMAT(`checktime`,'%Y-%m-%d %H:%i:%S') 
                FROM monitor_cpu WHERE CONCAT(`ip`,`checktime`) IN (SELECT CONCAT(`ip`,Max(`checktime`)) 
                FROM monitor_cpu GROUP BY `ip`);"""
                self.cursor.execute(_querysql)
            if self.ip:
                _load_cpu_result = self.dictfetchall()
                return _load_cpu_result[0]
            else:
                _load_cpu_result = self.cursor.fetchall()
                return _load_cpu_result
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()

    def load_cpu_loadavg_range(self):
        try:
            _querysql = """SELECT `load_1`,`load_5`,`load_15` FROM monitor_cpu WHERE `ip`='%s' AND 
            (DATE_FORMAT(`checktime`,'%%Y-%%m-%%d %%H:%%i:%%S') BETWEEN '%s' AND '%s');""" % (self.ip, self.ts, self.te)
            self.cursor.execute(_querysql)
            _load_cpu_loadavg_result = self.cursor.fetchall()
            return _load_cpu_loadavg_result
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()

    def load_cpu_time_range(self):
        try:
            _querysql = """SELECT `p_user`,`p_system`,`p_nice`,`p_idle`,`p_iowait`,`p_irq`,`p_softirq`,`p_steal` 
            FROM monitor_cpu WHERE `ip`='%s' AND (DATE_FORMAT(`checktime`, '%%Y-%%m-%%d %%H:%%i:%%S') 
            BETWEEN '%s' AND '%s');""" % (self.ip, self.ts, self.te)
            self.cursor.execute(_querysql)
            _load_cpu_time_result = self.cursor.fetchall()
            return _load_cpu_time_result
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()

    def load_disk(self):
        """读取磁盘信息"""
        try:
            if self.ip:
                _querysql = """SELECT `diskmount`,`diskusage`,DATE_FORMAT(`checktime`,'%%Y-%%m-%%d %%H:%%i:%%S') 
                AS `checktime` FROM monitor_disk WHERE `checktime` IN (SELECT Max(`checktime`) FROM monitor_disk 
                GROUP BY `ip`) AND `ip` = '%s';""" % self.ip
            else:
                _querysql = """SELECT `ip`,`diskmount`,`diskusage`,DATE_FORMAT(`checktime`,'%Y-%m-%d %H:%i:%S') 
                AS `checktime` FROM monitor_disk WHERE CONCAT(`ip`,`checktime`) IN (SELECT CONCAT(`ip`,Max(`checktime`)) 
                FROM monitor_cpu GROUP BY `ip`);"""
            self.cursor.execute(_querysql)
            if self.ip:
                _load_disk_result = self.dictfetchall()
                return _load_disk_result[0]
            else:
                _load_disk_result = self.cursor.fetchall()
                return _load_disk_result
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()

    def load_memory(self):
        """读取内存信息需进行单位换算,使用原生SQL,注意由于%和%%使用的不同"""
        try:
            if self.ip:
                _querysql = """SELECT `total`,`available`,`used`,`free`,`active`,`inactive`,`buffers`,`cached`,
                `shared`,`slab`,DATE_FORMAT(`checktime`,'%%Y-%%m-%%d %%H:%%i:%%S') AS `checktime` FROM 
                monitor_memory WHERE `checktime` IN (SELECT Max(`checktime`) FROM monitor_disk 
                GROUP BY `ip`) AND `ip` = '%s';""" % self.ip
            else:
                _querysql = """SELECT `ip`,`total`,`available`,`used`,`free`,`active`,`inactive`,`buffers`,`cached`,
                `shared`,`slab`,DATE_FORMAT(`checktime`,'%Y-%m-%d %H:%i:%S') FROM monitor_memory WHERE 
                CONCAT(`ip`,`checktime`) IN (SELECT CONCAT(`ip`,Max(`checktime`)) FROM monitor_cpu GROUP BY `ip`);"""
            self.cursor.execute(_querysql)
            if self.ip:
                _load_memory_result = self.dictfetchall()
                return _load_memory_result[0]
            else:
                _load_memory_result = self.cursor.fetchall()
                return _load_memory_result
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()

    def load_network(self):
        """读取网卡信息"""
        try:
            if self.ip:
                _querysql = """SELECT `netpic`,`netusage`,DATE_FORMAT(`checktime`,'%%Y-%%m-%%d %%H:%%i:%%S') 
                AS `checktime` FROM monitor_network WHERE `checktime` IN (SELECT  Max(`checktime`) FROM 
                monitor_network GROUP BY `IP`) AND `ip` = '%s';""" % self.ip
            else:
                _querysql = """SELECT `ip`,`netpic`,`netusage`,DATE_FORMAT(`checktime`,'%Y-%m-%d %H:%i:%S') 
                AS `checktime` FROM monitor_network WHERE CONCAT(`ip`,`checktime`) IN (SELECT 
                CONCAT(`ip`,Max(`checktime`)) FROM monitor_cpu GROUP BY `ip`);"""
            self.cursor.execute(_querysql)
            if self.ip:
                _load_network_result = self.dictfetchall()
                return _load_network_result[0]
            else:
                _load_network_result = self.cursor.fetchall()
                return _load_network_result
        except Exception as error:
            print(error)
        finally:
            self.cursor.close()
