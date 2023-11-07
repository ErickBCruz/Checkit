import uuid
from dashboard.models import DeviceMaintenance


class MaintenanceService():
    def __init__(self) -> None:
        pass
    
    def generate_random_ticket(self) -> str:
        ticket = uuid.uuid4().hex[:8].upper()
        return ticket
    
    def get_mainenance_status_by_ticket(self, ticket: str) -> str:
        maintenance = DeviceMaintenance.objects.get(ticket=ticket)
        return maintenance