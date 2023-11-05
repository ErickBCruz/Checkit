from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("pricing", views.pricing_view, name="pricing"),
    path("register-enterprise", views.register_enterprise_view, name="register-enterprise"),
    path("register-client", views.register_client_view, name="register-client")
]
