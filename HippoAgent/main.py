# -*- encoding:utf-8 -*-
import threading
import hippoagent


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
    t = 20                                    # 后期变更为settings
    timer = threading.Timer(1, fun_timer)
    timer.start()