from django.contrib import admin
from .models import Device, DeviceBrand, DeviceMaintenance


admin.site.register(Device)
admin.site.register(DeviceBrand)
admin.site.register(DeviceMaintenance)
