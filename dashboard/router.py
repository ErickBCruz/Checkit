from django.urls import path
from .views import (
    dashboard_common_views,
    dashboard_devices_views,
    dashboard_profile_views,
    dashboard_repair_enterprises_views,
)

urlpatterns = [
    path("home", dashboard_common_views.dashboard_home_view, name="dashboard-home"),
    path("logout", dashboard_common_views.logout_view, name="dashboard-logout"),
    path("profile", dashboard_profile_views.profile_view, name="dashboard-profile"),
    path("devices", dashboard_devices_views.devices_view, name="dashboard-devices"),
    path(
        "repair-enterprises",
        dashboard_repair_enterprises_views.repair_enterprises_view,
        name="dashboard-repair-enterprises",
    ),
]
