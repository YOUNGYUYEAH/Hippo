# -*- encoding:utf-8 -*-
from django.db import models


class Info(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=200, verbose_name="主机名")
    ip = models.CharField(max_length=20, unique=True, verbose_name="IP")
    # 调整一对多关系
    platform = models.CharField(max_length=500, verbose_name="系统信息")
    type = models.CharField(max_length=50, verbose_name="操作系统")
    kernel = models.CharField(max_length=200, verbose_name="内核版本")
    arch = models.CharField(max_length=30, verbose_name="架构")
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateField(null=True, verbose_name="基本信息更新时间")
    status = models.BooleanField(default=True, verbose_name="机器状态")
    remark = models.TextField(null=True, verbose_name="描述")

    class Meta:
        db_table = 'monitor_info'


class Cpu(models.Model):
    ip = models.CharField(max_length=20, verbose_name="主机ip")
    load_1 = models.CharField(max_length=20, verbose_name="1min负载")
    load_5 = models.CharField(max_length=20, verbose_name="5min负载")
    load_15 = models.CharField(max_length=20, verbose_name="15min负载")
    count = models.CharField(max_length=4, verbose_name="cpu核数")
    p_user = models.FloatField(verbose_name="us百分比")
    p_nice = models.FloatField(verbose_name="ni百分比")
    p_system = models.FloatField(verbose_name="sy百分比")
    p_idle = models.FloatField(verbose_name="id百分比")
    p_iowait = models.FloatField(verbose_name="wa百分比")
    p_irq = models.FloatField(verbose_name="hi百分比")
    p_softirq = models.FloatField(verbose_name="si百分比")
    p_steal = models.FloatField(verbose_name="st百分比")
    checktime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'monitor_cpu'


class Memory(models.Model):
    ip = models.CharField(max_length=20, verbose_name="主机ip")
    total = models.BigIntegerField(verbose_name="总量")
    available = models.BigIntegerField(verbose_name="可使用的内存量")
    used = models.BigIntegerField(verbose_name="当前已使用的内存量")
    free = models.BigIntegerField(verbose_name="空闲或可使用的内存量")
    active = models.BigIntegerField(verbose_name="用户进程活动中的内存量")
    inactive = models.BigIntegerField(verbose_name="用户进程中非活动的内存量")
    buffers = models.BigIntegerField(verbose_name="块设备数据缓冲")
    cached = models.BigIntegerField(verbose_name="文件内容数据缓冲")
    shared = models.BigIntegerField(verbose_name="共享内存大小,用于进程间通信")
    slab = models.BigIntegerField(verbose_name="特权进程使用的内存量")
    checktime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'monitor_memory'


class Disk(models.Model):
    ip = models.CharField(max_length=20, verbose_name="主机ip")
    diskmount = models.CharField(max_length=100, verbose_name="磁盘挂载点")
    diskusage = models.CharField(max_length=1000, verbose_name="磁盘挂载点用量")
    checktime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'monitor_disk'


class Network(models.Model):
    ip = models.CharField(max_length=20, verbose_name="主机ip")
    netpic = models.CharField(max_length=100, verbose_name="网卡名列表")
    netusage = models.CharField(max_length=1000, verbose_name="网卡用量")
    checktime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'monitor_network'

