from django.contrib.auth.hashers import make_password
from .models import User


class UserService:
    def __init__(self):
        print("UserService init... 🚀")

    def createUser(self, **kwargs):
        user = User.objects.create(
            username=kwargs["username"],
            first_name=kwargs["first_name"],
            last_name=kwargs["last_name"],
            profile_image=kwargs["profile_image"],
            password=make_password(kwargs["password"]),
        )
        return user
