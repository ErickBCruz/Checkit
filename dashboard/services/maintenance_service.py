import uuid


class MaintenanceService():
    def __init__(self) -> None:
        pass
    
    def generate_random_ticket(self) -> str:
        ticket = uuid.uuid4().hex[:8].upper()
        return ticket