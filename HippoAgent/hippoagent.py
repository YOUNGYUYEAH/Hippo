# -*- encoding:utf-8 -*-
import psutil
import config
import os
import json

def systeminfo():
    """
    系统内核和版本,主机名,架构
    """
    import socket
    import platform
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((config.ServerHost, int(config.ServerPost)))
        owner_ip = s.getsockname()[0]
        _systeminfo = dict()
        _systeminfo['platform'] = platform.platform()
        _systeminfo['ip'] = owner_ip
        _systeminfo['type'] = platform.system()
        _systeminfo['hostname'] = platform.node()
        _systeminfo['kernel'] = platform.release()
        _systeminfo['arch'] = platform.processor()
        s.close()
        return _systeminfo
    except Exception as e:
        print(e)


def cpuinfo():
    """
    CPU和负载信息采集
    """
    import platform
    _cpuinfo = dict()
    if platform.system() == 'Linux':
        with open('/proc/loadavg', 'r') as f:
            _v = f.read().split()
            _cpuinfo['load_1'] = _v[0]
            _cpuinfo['load_5'] = _v[1]
            _cpuinfo['load_15'] = _v[2]
    _cpuinfo['count'] = psutil.cpu_count()
    time_percent = psutil.cpu_times_percent(interval=1)
    _cpuinfo['p_user'] = time_percent[0]
    _cpuinfo['p_nice'] = time_percent[1]
    _cpuinfo['p_system'] = time_percent[2]
    _cpuinfo['p_idle'] = time_percent[3]
    _cpuinfo['p_iowait'] = time_percent[4]
    _cpuinfo['p_irq'] = time_percent[5]
    _cpuinfo['p_softirq'] = time_percent[6]
    _cpuinfo['p_steal'] = time_percent[7]
    _cpuinfo['user'] = psutil.cpu_times().user
    _cpuinfo['nice'] = psutil.cpu_times().nice
    _cpuinfo['system'] = psutil.cpu_times().system
    _cpuinfo['idle'] = psutil.cpu_times().idle
    _cpuinfo['iowait'] = psutil.cpu_times().iowait
    _cpuinfo['irq'] = psutil.cpu_times().irq
    _cpuinfo['softirq'] = psutil.cpu_times().softirq
    _cpuinfo['steal'] = psutil.cpu_times().steal
    _cpu_times_total = 0
    for c in range(len(psutil.cpu_times())):
        _cpu_times_total += psutil.cpu_times()[c]
    _cpuinfo['total'] = _cpu_times_total
    return _cpuinfo


def meminfo():
    """
    机器内存,用量统计
    """
    _meminfo = dict()
    _meminfo['total'] = psutil.virtual_memory().total
    _meminfo['available'] = psutil.virtual_memory().available
    _meminfo['used'] = psutil.virtual_memory().used
    _meminfo['free'] = psutil.virtual_memory().free
    _meminfo['active'] = psutil.virtual_memory().active
    _meminfo['inactive'] = psutil.virtual_memory().inactive
    _meminfo['buffers'] = psutil.virtual_memory().buffers
    _meminfo['cached'] = psutil.virtual_memory().cached
    _meminfo['shared'] = psutil.virtual_memory().shared
    _meminfo['slab'] = psutil.virtual_memory().slab
    return _meminfo


def diskinfo():
    import subprocess
    import re
    _diskinfo = dict()
    diskusage = []
    diskmount = []
    for i in psutil.disk_partitions():
        mount_info = dict()
        inode_shell = "df -i | grep -w %s | awk '{print $(NF-1)}'" % (i[1], )
        subshell = subprocess.Popen([inode_shell], shell=True, stdout=subprocess.PIPE)
        inode = subshell.stdout.readline().decode("utf-8").split("\n")[0]
        if inode:
            mount_info['inode'] = inode
            mount_info['total'] = round(psutil.disk_usage(i[1]).total/pow(1024, 3), 2)
            mount_info['used'] = round(psutil.disk_usage(i[1]).used/pow(1024, 3), 2)
            mount_info['percent'] = psutil.disk_usage(i[1]).percent
            diskmount.append(i[1])
            diskusage.append(json.dumps(mount_info))
        else:
            pass
    _diskinfo["mount"] = diskmount
    _diskinfo["usage"] = diskusage
    return _diskinfo


# def diskinfo():
#     """
#     获取磁盘总量用量和空闲及其百分比,动态感知分区
#     """
#     import subprocess
#     import re
#     _diskinfo = dict()
#     _diskallusage = dict()
#     _diskiousage = dict()
#     device_regex = re.compile(r'sd[a-z]|vd[a-z]')
#     allpart = psutil.disk_partitions()
#     iopart = psutil.disk_io_counters(perdisk=True, nowrap=True)
#     for _io in iopart:
#         _iousage = dict()
#         device = _io
#         if re.match(device_regex, _io):
#             _iousage['read_count'] = iopart[device].read_count
#             _iousage['write_count'] = iopart[device].write_count
#             _iousage['read_bytes'] = iopart[device].read_bytes
#             _iousage['write_bytes'] = iopart[device].write_bytes
#             _iousage['read_time'] = iopart[device].read_time
#             _iousage['write_time'] = iopart[device].write_time
#             _iousage['read_merged_count'] = iopart[device].read_merged_count
#             _iousage['write_merged_count'] = iopart[device].write_merged_count
#             _iousage['busy_time'] = iopart[device].busy_time
#         if _iousage:
#             _diskiousage[device] = _iousage
#     _diskinfo['io'] = _diskiousage
#     for _part in allpart:
#         _partusage = dict()
#         mountpoint = _part[1]
#         inode_shell = "df -i |grep -w %s | awk '{print $(NF-1)}'" % (mountpoint,)
#         subshell = subprocess.Popen([inode_shell], shell=True, stdout=subprocess.PIPE)
#         inode_usage = subshell.stdout.readline()
#         inode_usage = inode_usage.decode('utf-8').split('\n')[0]
#         usage = psutil.disk_usage(mountpoint)
#         _partusage['total'] = round(usage[0]/pow(1024, 3), 2)
#         _partusage['used'] = round(usage[1]/pow(1024, 3), 2)
#         _partusage['free'] = round(usage[2]/pow(1024, 3), 2)
#         _partusage['percent'] = usage[3]
#         if inode_usage:
#             _partusage['inode'] = inode_usage
#         _diskallusage[mountpoint] = _partusage
#     _diskinfo['usage'] = _diskallusage
#     return _diskinfo


def netinfo():
    """
    获取网卡总量用量和流量情况,需要于下次采集进行运算
    """
    _netinfo = dict()
    _addr = psutil.net_if_addrs()
    _stat = psutil.net_if_stats()
    _netio = psutil.net_io_counters(pernic=True)
    for netport in _addr:
        _net_usage = dict()
        _net_usage['ipaddr'] = _addr[netport][0][1]
        _net_usage['speed'] = _stat[netport][2]
        _net_usage['bytes_sent'] = _netio[netport][0]
        _net_usage['bytes_recv'] = _netio[netport][1]
        _net_usage['packetes_sent'] = _netio[netport][2]
        _net_usage['packetes_recv'] = _netio[netport][3]
        _netinfo[netport] = _net_usage
    return _netinfo


def tcpinfo():
    """检查TCP连接状态"""
    pass


def monitorjson():
    _monitorjson = dict()
    _monitorjson['system'] = systeminfo()
    _monitorjson['cpu'] = cpuinfo()
    _monitorjson['memory'] = meminfo()
    _monitorjson['disk'] = diskinfo()
    _monitorjson['network'] = netinfo()
    _monitorjson['period'] = config.Period
    return json.dumps(_monitorjson)


def pusher():
    """
    数据传递方式: JSON串用POST传递到接口
    """
    import requests
    domain = config.ServerHost+":"+config.ServerPost
    uri = '/monitor/i'
    url = 'http://' + str(domain) + uri
    requests.post(url=url, data=monitorjson())


if __name__ == '__main__':
    print(monitorjson())
    # print(disk())
