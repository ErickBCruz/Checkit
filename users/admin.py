from django.contrib import admin
from .models import User, Client, Enterprise, EnterpiseFollowers, EnterpriseViews

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Enterprise)
admin.site.register(EnterpiseFollowers)
admin.site.register(EnterpriseViews)