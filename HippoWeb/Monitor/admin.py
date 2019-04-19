from django.contrib import admin
from HippoWeb.Monitor import models

admin.register(models.Info)
admin.register(models.Cpu)
admin.register(models.Memory)
admin.register(models.Disk)
admin.register(models.Network)
