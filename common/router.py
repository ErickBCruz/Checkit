from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("pricing", views.pricing_view, name="pricing"),
    path("register-options", views.register_options_view, name="register-options"),
]
