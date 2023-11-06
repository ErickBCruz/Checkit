from users.models import Enterprise
from users.models import EnterpiseFollowers
from users.models import EnterpriseViews

class EnterpriseService():
    def __init__(self):
        print("EnterpriseService init... 🚀")
        
    def get_enterprises(self):
        return Enterprise.objects.all()
    
    def get_enterprise_by_user(self, user):
        return Enterprise.objects.get(user=user)
    
    def get_enterprise_by_id(self, id):
        return Enterprise.objects.get(id=id)
    
    def is_enterprise(self, user):
        enterprise = Enterprise.objects.filter(user=user).exists()
        return enterprise
    
    def increase_views(self, enterprise):
        try: 
            views = EnterpriseViews.objects.get(enterprise=enterprise)
        except EnterpriseViews.DoesNotExist:
            views = EnterpriseViews.objects.create(enterprise=enterprise)   
        views.views += 1
        views.save()
        return views
    
    def add_follower(self, enterprise, client):
        follower = EnterpiseFollowers.objects.create(enterprise=enterprise, client=client)
        return follower
    
    def is_follower(self, enterprise, client):
        follower = EnterpiseFollowers.objects.filter(enterprise=enterprise, client=client).exists()
        return follower