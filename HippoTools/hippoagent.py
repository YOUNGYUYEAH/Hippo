# -*- encoding:utf-8 -*-
import os
import json


def systeminfo():
    import platform
    _systeminfo = dict()
    _systeminfo['platform'] = platform.platform()
    _systeminfo['type'] = platform.system()
    _systeminfo['hostname'] = platform.node()
    _systeminfo['kernel'] = platform.release()
    _systeminfo['arch'] = platform.processor()
    return _systeminfo


def cpuinfo():
    import psutil
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
    import psutil
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
    import psutil
    _diskinfo = dict()
    allpart = psutil.disk_partitions(all=False)
    for i in allpart:
        print(i)
    return _diskinfo


if __name__ == '__main__':
    print(systeminfo())
    print(cpuinfo())
    print(meminfo())
    print(diskinfo())
