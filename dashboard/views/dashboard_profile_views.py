from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from users.services.client_service import ClientService
from users.services.enterprise_service import EnterpriseService


@login_required(login_url="/login")
def profile_view(request):
    user = request.user
    is_enterprice = EnterpriseService().is_enterprise(user)
    personal_data = None

    if is_enterprice:
        personal_data = EnterpriseService().get_enterprise_by_user(user)
    else:
        is_client = ClientService().is_client(user)
        if is_client:
            personal_data = ClientService().get_client(user)

    context = {
        "user": user,
        "personal_data": personal_data,
        "is_enterprice": is_enterprice,
    }
    return render(request, "dashboard-profile.html", context)

