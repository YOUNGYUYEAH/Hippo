# -*- encoding:utf-8 -*-
import psutil


def systeminfo():
    import platform
    _systeminfo = dict()
    _systeminfo['platform'] = platform.platform()
    _systeminfo['type'] = platform.system()
    if platform.system() == "Linux":
        with open("/proc/loadavg", "r") as f:
            _v = f.read().split()
            load = dict()
            load["1min"] = _v[0]
            load["5min"] = _v[1]
            load["15min"] = _v[2]
        _systeminfo['loadavg'] = load
    _systeminfo['hostname'] = platform.node()
    _systeminfo['kernel'] = platform.release()
    _systeminfo['arch'] = platform.processor()
    return _systeminfo


def cpuinfo():
    _cpuinfo = dict()
    _cpuinfo['count'] = psutil.cpu_count()                # 逻辑核数
    _cpuinfo['user'] = psutil.cpu_times().user
    _cpuinfo['nice'] = psutil.cpu_times().nice
    _cpuinfo['system'] = psutil.cpu_times().system
    _cpuinfo['idle'] = psutil.cpu_times().idle
    _cpuinfo['iowait'] = psutil.cpu_times().iowait
    _cpuinfo['irq'] = psutil.cpu_times().irq
    _cpuinfo['softirq'] = psutil.cpu_times().softirq
    _cpuinfo['steal'] = psutil.cpu_times().steal
    return _cpuinfo


def meminfo(unit="mb"):
    _meminfo = dict()
    _meminfo['total'] = psutil.virtual_memory().total
    _meminfo['available'] = psutil.virtual_memory().available
    _meminfo['used'] = psutil.virtual_memory().used
    _meminfo['free'] = psutil.virtual_memory().free
    _meminfo['active'] = psutil.virtual_memory().active
    _meminfo['inactive'] = psutil.virtual_memory().inactive
    _meminfo['huffers'] = psutil.virtual_memory().buffers
    _meminfo['cached'] = psutil.virtual_memory().cached
    _meminfo['shared'] = psutil.virtual_memory().shared
    _meminfo['slab'] = psutil.virtual_memory().slab
    if unit in ["mb", "Mb", "MB", "M"]:
        for k, v in enumerate(_meminfo):
            _meminfo[v] = round(int(_meminfo[v])/1024/1024, 1)
        return _meminfo
    elif unit in ["gb", "Gb", "GB", "G"]:
        for k, v in enumerate(_meminfo):
            _meminfo[v] = round(int(_meminfo[v])/1024/1024/1024, 1)
        return _meminfo


def diskinfo():
    _diskinfo = dict()
    allpart = psutil.disk_partitions()
    for _part in allpart:
        _diskusage = dict()
        mountpoint = _part[1]
        usage = psutil.disk_usage(mountpoint)
        _diskusage["total"] = round(usage[0]/1024/1024/1024, 1)
        _diskusage["used"] = round(usage[1]/1024/1024/1024, 1)
        _diskusage["free"] = round(usage[2]/1024/1024/1024, 1)
        _diskusage["percent"] = usage[3]
        _diskinfo[mountpoint] = _diskusage
    return _diskinfo


def netinfo():
    _netinfo = dict()
    _addr = psutil.net_if_addrs()
    _stat = psutil.net_if_stats()
    _netio = psutil.net_io_counters(pernic=True)
    for netport in _addr:
        _net_usage = dict()
        _net_usage["ipaddr"] = _addr[netport][0][1]
        _net_usage["speed"] = _stat[netport][2]
        _net_usage["bytes_sent"] = _netio[netport][0]
        _net_usage["bytes_recv"] = _netio[netport][1]
        _net_usage["packetes_sent"] = _netio[netport][2]
        _net_usage["packetes_recv"] = _netio[netport][3]
        _netinfo[netport] = _net_usage
    return _netinfo


def info_json():
    import json
    server_info = dict()
    server_info["SYSTEM"] = systeminfo()
    server_info["CPU"] = cpuinfo()
    server_info["MEM"] = meminfo()
    server_info["DISK"] = diskinfo()
    server_info["NET"] = netinfo()
    return json.dumps(server_info)


if __name__ == '__main__':
    info_json()
