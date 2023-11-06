from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.utils.enterprise_facade import EnterpriseFacade
import folium

from common.services.common_service import CommonService
from users.services.enterprise_service import EnterpriseService
from users.services.client_service import ClientService

common_service = CommonService()
enterprise_service = EnterpriseService()
client_service = ClientService()
default_latitude = common_service.default_latitude
default_longitude = common_service.default_longitude


@login_required(login_url="/login")
def repair_enterprises_view(request):
    m = folium.Map(location=[default_latitude, default_longitude], zoom_start=13)

    current_latitude = default_latitude
    current_longitude = default_longitude

    current_client = client_service.get_client(request.user)

    if current_client.latitude and current_client.longitude:
        current_latitude = current_client.latitude
        current_longitude = current_client.longitude

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

            popup_content = f"""
            <section>
                <div class="container p-1 h-100">
                    <div class="row h-100 justify-content-center align-items-center">
                        <div class="col-12 text-center">
                            <img src="{profile_image}" width="60px" class="img-fluid rounded-circle mx-auto" alt="Imagen de perfil">
                        </div>
                        <div class="col-12 text-center">
                            <p class="fs-italic">"{enterprise.slogan}"</p>
                        </div>
                        <div class="col-12 text-center">
                            <h5>{name}</h5>
                            <p>{enterprise_type}</p>
                            <p>{enterprise.address}</p>
                            <p>{enterprise.phone}</p>
                        </div>
                        <div class="col-12 text-center">
                            <a class="btn btn-info" type="button" href="/dashboard/enterprise/{enterprise.id}" target="_blank">
                                <i class="fa-solid fa-eye" style="color: #ffffff;"></i>
                            </a>

                            <a class="btn btn-success" type="button" href="https://wa.me/{enterprise.phone}"
                            target="_blank"
                            >
                                <i class="fa-brands fa-whatsapp" style="color: #ffffff;"></i>
                            </a>
                        </div>
                </div>
            </section>
            """

            folium.Marker(
                location=[latitude, longitude],
                tooltip=folium.Tooltip(
                    tooltip,
                    style="font-size: 7px;",
                    sticky=True,
                ),
                popup=folium.Popup(popup_content, max_width=500),
                icon=custom_marker,
            ).add_to(m)

    context = {
        "map": m._repr_html_(),
        "distance": int(distance / 1000),
        "near_enterprises_count": near_ent_count,
        "near_technicians_count": near_techn_count,
    }
    return render(request, "dashboard-repair-enterprises.html", context)


def enterprise_detail_view(request, id):
    enterprise = enterprise_service.get_enterprise_by_id(id)

    context = {
        "enterprise": enterprise,
    }

    return render(request, "enterprise-detail.html", context)
