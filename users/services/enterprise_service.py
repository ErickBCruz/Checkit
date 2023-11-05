from users.models import Enterprise

class EnterpriseService():
    def __init__(self):
        print("EnterpriseService init... 🚀")
        
    def get_enterprises(self):
        return Enterprise.objects.all()
    
    def get_enterprise_by_user(self, user):
        return Enterprise.objects.get(user=user)
    
    def is_enterprise(self, user):
        enterprise = Enterprise.objects.filter(user=user).exists()
        return enterprise