from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.utils.enterprise_facade import EnterpriseFacade
import folium

from common.services.common_service import CommonService
from users.services.enterprise_service import EnterpriseService

common_service = CommonService()
enterprise_service = EnterpriseService()
default_latitude = common_service.default_latitude
default_longitude = common_service.default_longitude

@login_required(login_url="/login")
def repair_enterprises_view(request):
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

    enterprise_facade = EnterpriseFacade(common_service, enterprise_service)

    (
        enterprises,
        near_ent_count,
        near_techn_count,
    ) = enterprise_facade.get_nearby_enterprises(
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

            tooltip = f""" <strong>{enterprise_type}: {name}</strong> <br>
            {enterprise.address}
            """

            folium.Marker(
                location=[latitude, longitude],
                tooltip=folium.Tooltip(
                    tooltip,
                    style="font-size: 7px;",
                    sticky=True,
                ),
                icon=custom_marker,
            ).add_to(m)

    context = {
        "map": m._repr_html_(),
        "distance": int(distance / 1000),
        "near_enterprises_count": near_ent_count,
        "near_technicians_count": near_techn_count,
    }
    return render(request, "dashboard-repair-enterprises.html", context)

