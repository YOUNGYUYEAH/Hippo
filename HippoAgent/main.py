# -*- encoding:utf-8 -*-
import threading
import hippoagent
import config


def fun_timer():
    """定时器执行监控"""
    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        hippoagent.sendjson()
    except Exception as e:
        print(e)
    global timer
    timer = threading.Timer(t, fun_timer)
    timer.start()


if __name__ == '__main__':
    t = int(config.Period)
    timer = threading.Timer(1, fun_timer)
    timer.start()
