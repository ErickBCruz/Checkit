from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required(login_url="/login")
def repair_enterprises_view(request):
    return render(request, "dashboard-repair-enterprises.html")

