# -*- encoding:utf-8 -*-
import hippoagent
import threading
import datetime


def fun_timer():
    """定时器执行监控"""
    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    hippoagent.influxdb()
    global timer
    timer = threading.Timer(t, fun_timer)
    timer.start()


if __name__ == '__main__':
    t = 20                                   # 后期变更为setting
    timer = threading.Timer(1, fun_timer)
    timer.start()
