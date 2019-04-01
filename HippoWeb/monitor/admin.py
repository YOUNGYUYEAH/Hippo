from django.contrib import admin
from HippoWeb.monitor import models

admin.register(models.info)
admin.register(models.cpu)
admin.register(models.memory)
