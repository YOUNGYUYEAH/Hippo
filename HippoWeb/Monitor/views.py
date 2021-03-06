# -*- encoding:utf-8 -*-
import json
import numpy as np
import datetime
from HippoWeb.Monitor import models
from HippoWeb.Monitor import MonitorORM
from django.shortcuts import HttpResponse, render
from django.contrib.auth.decorators import login_required
from HippoWeb.forms import HostModeForm, DateTimeForm


def collect(req):
    """接收agent数据的接口,仅接收方法为POST的请求,将数据判断后入库."""
    if req.method == 'POST':
        if req.body:
            try:
                monitorjson = json.loads(req.body, encoding='utf-8')
                monitorjson_system = monitorjson['system']
                if models.Info.objects.filter(ip=monitorjson_system['ip']):
                    # 需要判断新的数据是否跟源数据不同,若不同需要更新.
                    s = MonitorORM.SaveData(monitorjson)
                    s.save_all()
                    response = HttpResponse()
                    response.status_code = 200
                    return response
                else:
                    # 若不存在对应IP数据,则进行添加,顺便存入数据,返回API正常.
                    models.Info.objects.create(
                        host=monitorjson_system['hostname'],
                        ip=monitorjson_system['ip'],
                        platform=monitorjson_system['platform'],
                        type=monitorjson_system['type'],
                        kernel=monitorjson_system['kernel'],
                        arch=monitorjson_system['arch'],
                    )
                    s = MonitorORM.SaveData(monitorjson)
                    s.save_all()
                    response = HttpResponse()
                    response.status_code = 200
                    return response
            except Exception as error:
                # 请求异常,需要补充记录日志.
                print(error)
                response = HttpResponse("Bad Requests. \n")
                response.status_code = 412
                return response
        else:
            # 无任何请求报错.
            response = HttpResponse("Empty Request. =.=? \n")
            response.status_code = 412
            return response
    else:
        # 非POST方法报错.
        response = HttpResponse("API Error. :(  \n")
        response.status_code = 405
        return response


def monitor_host(_id):
    """前端返回需要搜索的服务器的id,通过id获取ip,然后获取值"""
    try:
        _ip = models.Info.objects.filter(id=_id).values('ip')[0]["ip"]
        title = ["Information", "CPU", "Memory", "Disk", "Network"]
        # 定义查询服务器详情页面时候的数据信息
        index = dict()
        index["Information"] = """{"IP":"ip", "Hostname":"host", "OS":"type", "Kernel":"platform", "Arch":"arch",
         "Status":"status", "Createtime":"createtime", "Updatetime":"updatetime", "Remark":"remark"}"""
        index["CPU"] = """{"Count":"count", "Load":"load_1", "Load":"load_5", "Load":"load_15", 
        "user":"p_user", "system":"p_system", "nice":"p_nice", "idle":"p_idle", "iowait":"p_iowait", 
        "irq":"p_irq", "softirq":"p_softirq","steal":"p_steal"}"""
        index["Memory"] = """{"Total":"total", "Available":"available", "Used":"used", "Free":"free", "Active":"active", 
        "Inactive":"inactive", "Buffers":"buffers", "Cached":"cached", "Shared":"shared", "Slab":"slab"}"""
        index["Disk"] = """{"Mount":"diskmount", "Percent":"percent", "Total":"total", "Used":"used", 
        "Inode":"inode"}"""
        index["Network"] = """{"Interface":"netpic", "ipaddr":"ipaddr", "Speed":"speed", "pps_sent[1s]":"pps_sent",
        "pps_recv[1s]":"pps_recv", "bps_sent[1s]":"bps_sent", "bps_recv[1s]":"bps_recv", "Error In":"errin",
        "Error Out":"errout"}"""
        _ip_info = MonitorORM.LoadData(_ip).load_info()
        _ip_cpu = MonitorORM.LoadData(_ip).load_cpu()
        _ip_memory = MonitorORM.LoadData(_ip).load_memory()
        _ip_disk = MonitorORM.LoadData(_ip).load_disk()
        _ip_network = MonitorORM.LoadData(_ip).load_network()
        hostdata = [_ip_info, _ip_cpu, _ip_memory, _ip_disk, _ip_network]
        _response = HttpResponse(json.dumps({'title': title,
                                             'value': hostdata,
                                             'index': index}),
                                 content_type='application/json')
        _response.status_code = 200
    except Exception as error:
        _response = HttpResponse(json.dumps({'error': error}))
        _response.status_code = 500
    return _response


def monitor_server():
    title = "Server List"
    thead = ["IP", "Hostname", "OS", "Kernel", "Arch", "Status", "Createtime", "Updatetime", "Remark"]
    try:
        s = MonitorORM.LoadData()
        _serverdata = s.load_info()
        serverdata = []
        for i in _serverdata:
            _ipvalue = [i["ip"], i["host"], i["type"], i["platform"], i["arch"], i["status"], i["ctime"],
                        i["utime"], i["remark"]]
            serverdata.append(_ipvalue)
    except Exception as error:
        serverdata = error
    _response = HttpResponse(json.dumps({'title': title,
                                         'head': thead,
                                         'value': serverdata}),
                             content_type='application/json')
    return _response


def monitor_cpu():
    title = "CPU List"
    thead = ["IP", "Load(1min)", "Load(5min)", "Load(15min)", "Count", "User", "System", "Nice","Idle", "IOwait",
             "Irq", "Softirq", "Steal", "Checktime"]
    try:
        s = MonitorORM.LoadData()
        cpudata = s.load_cpu()
    except Exception as error:
        cpudata = error
    _response = HttpResponse(json.dumps({'title': title,
                                         'head': thead,
                                         'value': cpudata}),
                             content_type='application/json')
    return _response


def monitor_memory():
    title = "Memory List"
    thead = ["IP", "Total", "Available", "Used", "Free", "Active", "Inactive", "Buffers", "Cached", "Shared",
             "Slab", "Checktime"]
    try:
        s = MonitorORM.LoadData()
        _data = s.load_memory()
        memorydata = []
        if _data:
            for ip in _data:
                _ipdata = []
                for value in ip:
                    _ipdata.append(value)
                memorydata.append(_ipdata)
    except Exception as error:
        memorydata = error
    _response = HttpResponse(json.dumps({'title': title,
                                         'head': thead,
                                         'value': memorydata}),
                             content_type='application/json')
    return _response


def monitor_disk():
    title = "Disk List"
    thead = ["IP", "Mount", "Usage", "Checktime"]
    try:
        s = MonitorORM.LoadData()
        _data = s.load_disk()
        diskdata = []
        for _ip in _data:
            arr = _ip[2].replace("'", '')
            ipvalue = [_ip[0], _ip[1][1:-1].split(","), arr, _ip[3]]
            diskdata.append(ipvalue)
    except Exception as error:
        diskdata = error
    _response = HttpResponse(json.dumps({'title': title,
                                         'head': thead,
                                         'value': diskdata}),
                             content_type='application/json')
    return _response


def monitor_network():
    title = "Network List"
    thead = ["IP", "Interface", "Netaddr", "Speed", "pps[1s] sent/recv", "bps[1s] sent/recv", "Err in/out", "Checktime"]
    try:
        s = MonitorORM.LoadData()
        _data = s.load_network()
        networkdata = []
        for _ip in _data:
            arr = _ip[2].replace("'", '')
            ipvalue = [_ip[0], _ip[1][1:-1].split(","), arr, _ip[3]]
            networkdata.append(ipvalue)
    except Exception as error:
        networkdata = error
    _response = HttpResponse(json.dumps({'title': title,
                                         'head': thead,
                                         'value': networkdata}),
                             content_type='application/json')
    return _response


def search(req):
    if req.is_ajax():
        if req.method == 'POST':
            search_type = req.POST.get('type')
            if search_type == "host":
                _id = req.POST.get('option')
                response = monitor_host(_id)
                return response
            elif search_type == "server":
                response = monitor_server()
                return response
            elif search_type == "cpu":
                response = monitor_cpu()
                return response
            elif search_type == "memory":
                response = monitor_memory()
                return response
            elif search_type == "disk":
                _response = monitor_disk()
                return _response
            elif search_type == "network":
                _response = monitor_network()
                return _response
            else:
                pass
        else:
            # 非POST方法报错.
            response = HttpResponse("API Error. :(  \n")
            response.status_code = 405
            return response
    else:
        # 仅接受AJAX.
        response = HttpResponse("ONLY AJAX. :(  \n")
        response.status_code = 405
        return response


def data(req):
    """通过查询返回数据"""
    hostmode_form = HostModeForm()
    return render(req, 'monitor/monitor_data.html', {'hostmode_form': hostmode_form})


def chart_cpu(ip, ts, te):
    _cpuval = dict()
    _cpu = MonitorORM.LoadData(ip=ip, time_start=ts, time_end=te).load_cpu_range()
    _cpuval["title"] = ""
    _cpuval["legend"] = ["checktime", "load_1", "load_5", "load_15", "us", "sy", "ni", "id", "wa", "hi", "si", "st"]
    _cpuval["axis"] = np.array(_cpu).tolist()
    _response = HttpResponse(json.dumps({'cpuval': _cpuval,
                                         'title': "CPU Used"}),
                             content_type='application/json')
    return _response


def chart_disk(ip, ts, te):
    try:
        _diskval = dict()
        _diskval["axis"] = []
        _diskval["legend"] = []
        _value = []
        _disk = MonitorORM.LoadData(ip=ip, time_start=ts, time_end=te).load_disk_used()
        _diskval["mount"] = np.transpose(list(_disk))[0][0]
        for d in _disk:
            _value.append(d[1].lstrip("['").rstrip("']").split("', '"))
        _diskval["value"] = np.transpose(_value).tolist()
        for i in _disk:
            _diskval["axis"].append(i[2])
        for m in _diskval["mount"].lstrip("[").rstrip("]").split(", "):
            _diskval["legend"].append(m+" Used")
            _diskval["legend"].append(m+" Total")
            _diskval["legend"].append(m+" Inode")
        _response = HttpResponse(json.dumps({'diskval': _diskval,
                                             'title': "Disk Used"}),
                                 content_type='application/json')
        return _response
    except Exception as e:
        print(e)


def chart_memory(ip, ts, te):
    try:
        _Memval = dict()
        _memval = dict()
        _Mem = MonitorORM.LoadData(ip=ip, time_start=ts, time_end=te).load_memory_used_free()
        _Memval["legend"] = ["checktime", "Used", "Free"]
        _Memval["axis"] = [list(Z) for Z in _Mem]
        _mem = MonitorORM.LoadData(ip=ip, time_start=ts, time_end=te).load_mem_used_free_buffer_cached()
        _memval["legend"] = ["checktime", "used", "free", "buffers", "cached"]
        _memval["axis"] = [list(z) for z in _mem]
        _response = HttpResponse(json.dumps({'memval': _memval,
                                             'Memval': _Memval,
                                             'title': "Memory Used"}),
                                 content_type='application/json')
        return _response
    except Exception as e:
        print(e)


def chart_network(ip, ts, te):
    try:
        _netval = dict()
        _netval["axis"] = []
        _netval["value"] = []
        _valuelist = []
        _net = MonitorORM.LoadData(ip=ip, time_start=ts, time_end=te).load_network_range()
        _netval["netpic"] = np.transpose(list(_net))[0][0]
        for n in _net:
            _netval["axis"].append(n[2])
            for N in n[1].lstrip("['").rstrip("']").split("', '"):
                _N = json.loads(N)
                _value = [_N["ipaddr"], _N["packetes_sent"], _N["packetes_recv"],
                          _N["bytes_sent"], _N["bytes_recv"], _N["errout"], _N["errin"],
                          _N["bps_sent"], _N["bps_recv"], _N["pps_sent"], _N["pps_recv"]]
                _valuelist.append(_value)
        print(_valuelist)
    except Exception as e:
        print(e)


def create(req):
    try:
        if req.is_ajax():
            if req.method == 'POST':
                chart_ip = req.POST.get('ip')
                chart_time = req.POST.get('time_range')
                chart_type = req.POST.get('type')
                if chart_time == "1hour":
                    ts = str((datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                    te = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    ts = chart_time.split(" - ")[0].lstrip().rstrip()
                    te = chart_time.split(" - ")[1].lstrip().rstrip()

                if chart_type == 'cpu':
                    _response = chart_cpu(chart_ip, ts, te)
                    return _response
                elif chart_type == "disk":
                    _response = chart_disk(chart_ip, ts, te)
                    return _response
                elif chart_type == 'memory':
                    _response = chart_memory(chart_ip, ts, te)
                    return _response
                elif chart_type == 'network':
                    _response = chart_network(chart_ip, ts ,te)
                    return _response
                else:
                    pass
            else:
                # 非POST方法报错.
                response = HttpResponse("API Error. :(  \n")
                response.status_code = 405
                return response
        else:
            # 仅接受AJAX.
            response = HttpResponse("ONLY AJAX. :(  \n")
            response.status_code = 405
            return response
    except Exception as e:
        print(e)


def chart(req):
    """根据查询数据出图"""
    _nowtime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    _hoursago = str((datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
    hostmode_form = HostModeForm()
    datetime_form = DateTimeForm()
    querytimedict = {"6Hours": 6, "1Day": 24, "1Week": 168, "2Weeks": 336}
    return render(req, 'monitor/monitor_chart.html', {'hostmode_form': hostmode_form,
                                                      'datetime_form': datetime_form,
                                                      'hoursago': _hoursago,
                                                      'nowtime': _nowtime,
                                                      'querytimeDict': querytimedict})

