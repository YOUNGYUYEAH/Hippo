# -*- encoding:utf-8 -*-
import hippoagent
import threading
import sys


def fun_timer(time=60):
    """定时器执行监控"""
    print(hippoagent.createjson())
    global timer
    timer = threading.Timer(time, fun_timer)
    timer.start()


if __name__ == '__main__':
    option = sys.argv[1]
    timer = threading.Timer(1, fun_timer(option))
    timer.start()
