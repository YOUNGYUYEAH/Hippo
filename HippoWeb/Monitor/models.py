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
    period = models.CharField(max_length=10, verbose_name="记录检查时间间隔")
    remark = models.TextField(null=True, verbose_name="描述")

    class Meta:
        db_table = 'monitor_info'


class Cpu(models.Model):
    ip = models.CharField(max_length=20, verbose_name="主机ip")
    loadavg = models.CharField(max_length=500, verbose_name="负载")
    count = models.CharField(max_length=4, verbose_name="cpu核数")
    user = models.FloatField(verbose_name="用户态使用cpu时间比")
    system = models.FloatField(verbose_name="系统态使用cpu时间比")
    nice = models.FloatField(verbose_name="用于nice加权的进程分配的用户态cpu时间比")
    idle = models.FloatField(verbose_name="空闲的cpu时间比")
    iowait = models.FloatField(verbose_name="cpu等待磁盘写入时间比")
    irq = models.FloatField(verbose_name="硬中断消耗时间比")
    softirq = models.FloatField(verbose_name="软中断消耗时间比")
    steal = models.FloatField(verbose_name="虚拟机偷取时间比")
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
    """
    建表语句
    CREATE TABLE `monitor_disk` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `ip` varchar(20) NOT NULL,
    `diskusage` json DEFAULT NULL,
    `iousage` json DEFAULT NULL,
    `checktime` datetime(6) DEFAULT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8

    SELECT `ip`,`diskusage`->'$."/".free' FROM Hippo.monitor_disk limit 1;
    注意根目录需要加双引号""
    """
    ip = models.CharField(max_length=20, verbose_name="主机ip")
    diskusage = models.TextField(verbose_name="磁盘用量JSON串")
    iousage = models.TextField(verbose_name="磁盘IO用量JSON串")
    checktime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'monitor_disk'


class Network(models.Model):
    """network使用JSON类型"""
    ip = models.CharField(max_length=20, verbose_name="主机ip")
    network = models.TextField(verbose_name="网卡情况JSON串")
    checktime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'monitor_network'

