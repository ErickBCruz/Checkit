from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import folium


def index(request):
    m = folium.Map(location=[4.142, -73.62664], zoom_start=13)
    context = {"map": m._repr_html_()}
    return render(request, "index.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard-home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard-home")
        else:
            print("Error")
    return render(request, "login.html")
