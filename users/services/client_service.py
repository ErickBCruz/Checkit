from users.models import Client


class ClientService:
    def __init__(self):
        print("ClientService init... 🚀")

    def createClient(self, **kwargs):
        client = Client.objects.create(
            phone=kwargs["phone"],
            address=kwargs["address"],
            latitude=kwargs["latitude"],
            longitude=kwargs["longitude"],
            birthday=kwargs["birthday"],
            user=kwargs["user"],
        )
        return client
    
    def is_client(self, user):
        client = Client.objects.filter(user=user).exists()
        return client
    
    def get_client(self, user):
        client = Client.objects.get(user=user)
        return client
