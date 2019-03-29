# -*- encoding:utf-8 -*-
import psutil
# 校验数值正常项目会添加 #check


def systeminfo():
    """系统内核和版本,主机名,架构"""
    import platform
    _systeminfo = dict()
    _systeminfo['platform'] = platform.platform()           # check
    _systeminfo['type'] = platform.system()                 # check
    _systeminfo['hostname'] = platform.node()               # check
    _systeminfo['kernel'] = platform.release()              # check
    _systeminfo['arch'] = platform.processor()              # check
    return _systeminfo


def cpuinfo():
    import platform
    _cpuinfo = dict()
    if platform.system() == "Linux":                        # check
        with open("/proc/loadavg", "r") as f:
            _v = f.read().split()
            load = dict()
            load["1min"] = _v[0]
            load["5min"] = _v[1]
            load["15min"] = _v[2]
        _cpuinfo['loadavg'] = load
    _cpuinfo['count'] = psutil.cpu_count()
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


def meminfo(unit="mb"):                                   # 后期设置为setting
    """机器内存,用量统计,可以设置MB或GB单位"""
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
    if unit in ["mb", "Mb", "MB", "M"]:
        for k, v in enumerate(_meminfo):
            _meminfo[v] = round(int(_meminfo[v])/1024/1024, 2)
        return _meminfo
    elif unit in ["gb", "Gb", "GB", "G"]:
        for k, v in enumerate(_meminfo):
            _meminfo[v] = round(int(_meminfo[v])/1024/1024/1024, 2)
        return _meminfo


def diskinfo():
    """获取磁盘总量用量和空闲及其百分比,动态"""
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


def minitor_json():
    import json
    _minitor_json = dict()
    _minitor_json["system"] = systeminfo()
    _minitor_json["cpu"] = cpuinfo()
    _minitor_json["memory"] = cpuinfo()
    _minitor_json["disk"] = cpuinfo()
    _minitor_json["network"] = cpuinfo()
    return json.dumps(_minitor_json)


def influxdb():
    from influxdb import InfluxDBClient
    client = InfluxDBClient(host='192.168.80.100', port=8086, username='influxdb',
                            password='531144968', database='Hippoagent')       # 后期变更为setting
    influx_data = [{'measurement': 'serverinfo',
                    'tags': {"ip": "192.168.80.100"},
                   'fields': {
                       "system": str(systeminfo()),
                       "cpu": str(cpuinfo()),
                       "memory": str(meminfo()),
                       "disk": str(diskinfo()),
                       "network": str(netinfo())
                   }}]
    client.write_points(influx_data)
    client.close()


if __name__ == '__main__':
    print(cpuinfo())
    # print(diskinfo())
    # print(netinfo())
