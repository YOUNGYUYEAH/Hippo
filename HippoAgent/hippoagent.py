# -*- encoding:utf-8 -*-
import psutil
import config
import json
import platform


def systeminfo():
    """系统内核和版本,主机名,架构,windows下也正常"""
    import socket
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


def cpuinfo():
    """CPU和负载信息采集,Linux才有loadavg,windows的cpu信息较少"""
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
    elif platform.system() == 'Windows':
        _cpuinfo['count'] = psutil.cpu_count()
        time_percent = psutil.cpu_times_percent(interval=1)
        _cpuinfo['p_user'] = time_percent[0]
        _cpuinfo['p_system'] = time_percent[1]
        _cpuinfo['p_idle'] = time_percent[2]
        _cpuinfo['p_interrupt'] = time_percent[3]
        _cpuinfo['p_dpc'] = time_percent[4]
    return _cpuinfo


def meminfo():
    """机器内存,用量统计"""
    _meminfo = dict()
    _meminfo['total'] = psutil.virtual_memory().total
    _meminfo['available'] = psutil.virtual_memory().available
    _meminfo['used'] = psutil.virtual_memory().used
    _meminfo['free'] = psutil.virtual_memory().free
    if platform.system() == 'Linux':
        _meminfo['active'] = psutil.virtual_memory().active
        _meminfo['inactive'] = psutil.virtual_memory().inactive
        _meminfo['buffers'] = psutil.virtual_memory().buffers
        _meminfo['cached'] = psutil.virtual_memory().cached
        _meminfo['shared'] = psutil.virtual_memory().shared
        _meminfo['slab'] = psutil.virtual_memory().slab
    return _meminfo


def diskinfo():
    """windows使用自带参数检测,Linux调用subprocess检查磁盘信息,将挂载点和挂载点数据分开存储,过滤/boot和type为tmpfs的衍生挂载点"""
    _diskinfo = dict()
    diskusage = []
    diskmount = []
    if platform.system() == 'Linux':
        import subprocess
        for i in psutil.disk_partitions():
            if i[1] != "/boot":
                _mount_info = dict()
                inode_shell = "df -i | grep -w %s | awk '{print $(NF-1)}'" % (i[1], )
                subshell = subprocess.Popen([inode_shell], shell=True, stdout=subprocess.PIPE)
                inode = subshell.stdout.readline().decode("utf-8").split("\n")[0]
                if inode:
                    _mount_info['inode'] = int(inode.split("%")[0])
                    _mount_info['total'] = psutil.disk_usage(i[1]).total
                    _mount_info['used'] = psutil.disk_usage(i[1]).used
                    _mount_info['percent'] = psutil.disk_usage(i[1]).percent
                    diskmount.append(i[1])
                    diskusage.append(json.dumps(_mount_info))
    elif platform.system() == 'Windows':
        for i in psutil.disk_partitions():
            if i[3] != "cdrom":
                _mount_info = dict()
                _mount_info['total'] = psutil.disk_usage(i[1]).total
                _mount_info['used'] = psutil.disk_usage(i[1]).used
                _mount_info['percent'] = psutil.disk_usage(i[1]).percent
                diskmount.append(i[1].split(':\\')[0])
                diskusage.append(json.dumps(_mount_info))
    _diskinfo["mount"] = diskmount
    _diskinfo["usage"] = diskusage
    return _diskinfo


def netinfo():
    """获取网卡总量用量和流量情况"""
    import time
    _netinfo = dict()
    netpic = []
    netusage = []
    _addr = psutil.net_if_addrs()
    _stat = psutil.net_if_stats()
    _netio1 = psutil.net_io_counters(pernic=True, nowrap=True)
    time.sleep(1)
    _netio2 = psutil.net_io_counters(pernic=True, nowrap=True)
    for netport in _addr:
        netpic.append(netport)
        _net_usage = dict()
        if platform.system() == 'Linux':
            _net_usage['ipaddr'] = _addr[netport][0][1]
        elif platform.system() == 'Windows':
            _net_usage['ipaddr'] = _addr[netport][1][1]
        _net_usage['speed'] = _stat[netport][2]
        _net_usage['bytes_sent'] = _netio2[netport][0]
        _net_usage['bytes_recv'] = _netio2[netport][1]
        _net_usage['packetes_sent'] = _netio2[netport][2]
        _net_usage['packetes_recv'] = _netio2[netport][3]
        _net_usage['errin'] = _netio2[netport][4]
        _net_usage['errout'] = _netio2[netport][5]
        _net_usage['bps_sent'] = _netio2[netport][0] - _netio1[netport][0]
        _net_usage['bps_recv'] = _netio2[netport][1] - _netio1[netport][1]
        _net_usage['pps_sent'] = _netio2[netport][2] - _netio1[netport][2]
        _net_usage['pps_recv'] = _netio2[netport][3] - _netio1[netport][3]
        netusage.append(json.dumps(_net_usage))
    _netinfo["pernic"] = netpic
    _netinfo["usage"] = netusage
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
