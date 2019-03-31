from django.db import models


class info(models.Model):
    id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=200, verbose_name="主机名")
    ip = models.CharField(max_length=20, unique=True, verbose_name="IP")
    platform = models.CharField(max_length=500, verbose_name="系统信息")
    type = models.CharField(max_length=50, verbose_name="操作系统")
    kernel = models.CharField(max_length=200, verbose_name="内核版本")
    arch = models.CharField(max_length=30, verbose_name="架构")
    create_time = models.DateField(auto_now_add=True, verbose_name="创建时间")
    status = models.BooleanField(default=True, verbose_name="机器状态")


class cpu(models.Model):
    ip = models.CharField(max_length=20, verbose_name="主机名")
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
    checktime = models.DateTimeField(auto_now_add=True)

