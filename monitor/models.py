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
