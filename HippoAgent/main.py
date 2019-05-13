# -*- encoding:utf-8 -*-
import sys
import threading
import hippoagent
import config


def subtimer():
    """定时器执行监控"""
    try:
        hippoagent.pusher()
    except Exception as e:
        print(e)
    global timer
    timer = threading.Timer(t, subtimer)
    timer.start()


if __name__ == '__main__':
    # 添加pid文件,判断程序是否启动,需要设置不允许重复启动
    if config.Switch == "On":
        print("定时器已启动..")
        t = int(config.Period)
        timer = threading.Timer(1, subtimer)
        timer.start()
    else:
        print("定时器已关闭,请在config中配置为On")
        sys.exit()
