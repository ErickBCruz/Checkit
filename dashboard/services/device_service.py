from dashboard.models import Device
from django.core.paginator import Paginator
from dashboard.services.maintenance_service import MaintenanceService


class DeviceService:
    def __init__(self):
        print("DeviceService init... 🚀")

    def get_user_devices(self, user):
        return (
            Device.objects.filter(owner=user).order_by("-created_at").order_by("status")
        )
        
    def get_device(self, device_id):
        return Device.objects.get(id=device_id)

    def get_paged_user_devices(self, user, page, per_page):
        devices = self.get_user_devices(user)

        for device in devices:
            status = device.maintenance = MaintenanceService().get_status_from_device(
                device
            )
            if not status or status == None:
                device.status = "-1"
            else:
                device.status = str(status)
        paginator = Paginator(devices, per_page)
        return paginator.get_page(page)
