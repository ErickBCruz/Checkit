from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from users.forms import EnterpriseRegisterForm
from users.utils.enterprise_facade import EnterpriseFacade

from .services import CommonService

import folium


common_service = CommonService()
default_latitude = common_service.default_latitude
default_longitude = common_service.default_longitude


def index(request):
    m = folium.Map(location=[default_latitude, default_longitude], zoom_start=13)
    

    current_latitude, current_longitude = common_service.get_current_position(request)

    distance = request.GET.get("distance-range")
    distance = (int(distance) * 1000) if distance else 1000

    folium.Marker(
        location=[current_latitude, current_longitude],
        tooltip=folium.Tooltip(
            f"Tu ubicación",
            style="font-size: 7px;",
            sticky=True,
        ),
        icon=folium.Icon(color="red", icon="home"),
    ).add_to(m)

    folium.Circle(
        location=[current_latitude, current_longitude],
        radius=distance,
        color="#3186cc",
        fill=True,
        fill_color="#3186cc",
    ).add_to(m)

    enterprise_facade = EnterpriseFacade(common_service)
    
    enterprises, near_ent_count, near_techn_count = enterprise_facade.get_nearby_enterprises(
        lat=current_latitude,
        lng=current_longitude,
        target=distance,
    )

    for enterprise in enterprises:
        if enterprise.latitude and enterprise.longitude:
            name = enterprise.enterprise_name
            latitude = enterprise.latitude
            longitude = enterprise.longitude

            profile_image = enterprise.user.profile_image.url
            profile_image = common_service.get_normalized_profile_image(profile_image)

            custom_marker = folium.CustomIcon(profile_image, icon_size=(50, 50))

            enterprise_type = "Empresa" if enterprise.type == "1" else "Técnico"

            folium.Marker(
                location=[latitude, longitude],
                tooltip=folium.Tooltip(
                    f"{enterprise_type}: {name}", style="font-size: 7px;", sticky=True
                ),
                icon=custom_marker,
            ).add_to(m)

    context = {
        "map": m._repr_html_(),
        "distance": int(distance / 1000),
        "near_enterprises_count": near_ent_count,
        "near_technicians_count": near_techn_count
    }
    return render(request, "index.html", context)


def pricing_view(request):
    return render(request, "pricing.html")


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
            messages.error(request, "Nombre de usuario o contraseña incorrectos")
    return render(request, "login.html")


def register_enterprise_view(request):
    if request.method == "POST":
        form = EnterpriseRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Empresa registrada correctamente")
            return redirect("login")
    else:
        form = EnterpriseRegisterForm()
    return render(request, "register-enterprise.html", {"form": form})
