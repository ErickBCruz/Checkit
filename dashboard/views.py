from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def dashboard_home_view(request):
    user = request.user
    context = {"user": user}
    return render(request, "dashboard-home.html", context)

@login_required(login_url="/login")
def profile_view(request):
    user = request.user
    context = {"user": user}
    return render(request, "dashboard-profile.html", context)

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
