from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def dashboard_home_view(request):
    user = request.user
    context = {
        "user": user
    }
    return render(request, "dashboard-home.html", context)
