# -*- encoding:utf-8 -*-
import hippoagent
import threading


def fun_timer():
    print(hippoagent.createjson())
    global timer
    timer = threading.Timer(60, fun_timer)
    timer.start()


if __name__ == '__main__':
    timer = threading.Timer(1, fun_timer)
    timer.start()
