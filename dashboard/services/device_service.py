from dashboard.models import Device
from django.core.paginator import Paginator

class DeviceService:
    def __init__(self):
        print("DeviceService init... 🚀")

    def get_user_devices(self, user):
        return Device.objects.filter(owner=user).order_by("-created_at")

    def get_paged_user_devices(self, user, page, per_page):
        devices = self.get_user_devices(user)
        paginator = Paginator(devices, per_page)
        return paginator.get_page(page)
