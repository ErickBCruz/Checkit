from users.models import Enterprise

class EnterpriseService():
    def __init__(self):
        print("EnterpriseService init... 🚀")
        
    def get_enterprises(self):
        return Enterprise.objects.all()