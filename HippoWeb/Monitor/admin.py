from django.contrib import admin
from HippoWeb.Monitor import models

admin.register(models.info)
admin.register(models.cpu)
admin.register(models.memory)
admin.register(models.disk)
admin.register(models.network)
