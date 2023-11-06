from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.forms.device.create_divice_form import CreateDeviceForm

from dashboard.services.device_service import DeviceService
from users.services.client_service import ClientService

device_service = DeviceService()
client_service = ClientService()


@login_required(login_url="/login")
def devices_view(request):
    page_number = request.GET.get("page", 1)
    PER_PAGE = 2
    
    is_client = client_service.is_client(request.user)
    devices = None
    device_form = None

    if is_client:
        client = client_service.get_client(request.user)
        devices = device_service.get_paged_user_devices(client, page_number, PER_PAGE)
        device_form = CreateDeviceForm()
    
    context = {
        "devices": devices,
        "device_form": device_form,
    }

    return render(request, "dashboard-devices.html", context)
