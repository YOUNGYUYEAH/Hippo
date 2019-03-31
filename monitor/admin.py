from django.contrib import admin
from monitor import models


admin.register(models.info)
admin.register(models.cpu)
admin.register(models.memory)
