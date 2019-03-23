# -*- encoding:utf-8 -*-
import hippoagent
import threading


def fun_timer(t):
    """定时器执行监控"""
    print(hippoagent.createjson())
    global timer
    timer = threading.Timer(int(t), fun_timer(t))
    timer.start()


if __name__ == '__main__':
    time = 10
    timer = threading.Timer(1, fun_timer(time))
    timer.start()
