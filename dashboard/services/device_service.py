from dashboard.models import Device


class DeviceService:
    def __init__(self):
        print("DeviceService init... 🚀")
        
    def get_user_devices(self, user):
        return Device.objects.filter(user=user)
