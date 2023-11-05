from django.shortcuts import render

def devices_view(request):
    return render(request, "dashboard-devices.html")