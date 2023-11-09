import uuid
from dashboard.models import DeviceMaintenance
from django.core.paginator import Paginator
from dashboard.constants.device_constants import MAINTENANCE_STATUS

class MaintenanceService:
    def __init__(self) -> None:
        pass

    def generate_random_ticket(self) -> str:
        ticket = uuid.uuid4().hex[:8].upper()
        return ticket

    def get_mainenance_status_by_ticket(self, ticket: str) -> str:
        maintenance = DeviceMaintenance.objects.get(ticket=ticket)
        return maintenance
    
    def get_maintenance_by_ticket(self, ticket: str) -> str:
        maintenance = DeviceMaintenance.objects.get(ticket=ticket)
        return maintenance
    
    def get_status_from_device(self, device) -> str:
        maintenance = DeviceMaintenance.objects.filter(device=device).first()
        return maintenance.status if maintenance else None

    def get_maintenance_enterprise_devices(self, enterprise) -> list:
        devices = DeviceMaintenance.objects.filter(enterprise=enterprise).order_by("status")
        return devices
    
    def get_paged_maintenance_enterprise_devices(self, enterprise, page, per_page):
        devices = self.get_maintenance_enterprise_devices(enterprise)
        paginator = Paginator(devices, per_page)
        return paginator.get_page(page)
    
    def confirm_maintenance(self, device):
        maintenance = DeviceMaintenance.objects.filter(device=device).first()
        maintenance.status = MAINTENANCE_STATUS[1][0]
        maintenance.save()
