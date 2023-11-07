from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from dashboard.forms.device.create_divice_form import CreateDeviceForm

from dashboard.services.device_service import DeviceService
from dashboard.services.maintenance_service import MaintenanceService
from users.services.client_service import ClientService
from users.services.enterprise_service import EnterpriseService

device_service = DeviceService()
client_service = ClientService()
maintenance_service = MaintenanceService()
enterprise_service = EnterpriseService()


@login_required(login_url="/login")
def devices_view(request):
    page_number = request.GET.get("page", 1)
    PER_PAGE = 3

    is_client = client_service.is_client(request.user)
    devices = None
    device_form = None
    client = None

    if is_client:
        client = client_service.get_client(request.user)
        devices = device_service.get_paged_user_devices(client, page_number, PER_PAGE)
        device_form = CreateDeviceForm()

        if request.method == "POST":
            device_form = CreateDeviceForm(request.POST, request.FILES)
            if device_form.is_valid():
                device = device_form.save(commit=False)
                device.owner = client
                device.save()
                return redirect("dashboard-devices")
    else:
        enterprise = enterprise_service.get_enterprise_by_user(request.user)
        devices = (
            maintenance_service.get_paged_maintenance_enterprise_devices(
                enterprise, page_number, PER_PAGE
            )
        )    

    context = {
        "devices": devices,
        "device_form": device_form,
        "is_client": is_client,
    }

    return render(request, "dashboard-devices.html", context)
