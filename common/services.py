from users.models import Enterprise
from math import sin, cos, sqrt, asin, pi
from functools import reduce
import json


class CommonService:
    default_latitude = 4.14986
    default_longitude = -73.63647

    def __init__(self):
        print("CommonService init... 🚀")

    def get_enterprises(self):
        return Enterprise.objects.all()

    def get_normalized_profile_image(self, profile_image) -> str:
        split_profile_image = profile_image.split("/")
        split_profile_image.insert(6, "w_150,h_150,c_thumb,g_face,r_max")
        split_profile_image[-1] += ".png"
        profile_image = "/".join(split_profile_image)
        return profile_image

    def calculate_semiversen(self, **kwargs):
        r = 6371000
        c = pi / 180
        user_lat = float(kwargs.get("user_latitude"))
        user_lng = float(kwargs.get("user_longitude"))
        ent_lat = float(kwargs.get("enterprise_latitude"))
        ent_lng = float(kwargs.get("enterprise_longitude"))

        d = (
            2
            * r
            * asin(
                sqrt(
                    sin(c * (ent_lat - user_lat) / 2) ** 2
                    + cos(c * user_lat)
                    * cos(c * ent_lat)
                    * sin(c * (ent_lng - user_lng) / 2) ** 2
                )
            )
        )

        return d

    def get_current_position(self, request):
        current_position = request.COOKIES.get("geolocation")

        if not current_position or current_position is None:
            current_position = json.dumps(
                {"lat": self.default_latitude, "lng": self.default_longitude}
            )
            return self.default_latitude, self.default_longitude

        parsed_current_position = json.loads(current_position)

        current_latitude = parsed_current_position["lat"]
        current_longitude = parsed_current_position["lng"]

        return current_latitude, current_longitude
