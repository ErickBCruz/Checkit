class EnterpriseFacade:
    def __init__(self, common_service):
        self.common_service = common_service

    def get_nearby_enterprises(self, lat, lng, target=1000):
        all_enterprises = self.common_service.get_enterprises()
        near_enterprises = []

        for enterprise in all_enterprises:
            if enterprise.latitude and enterprise.longitude:
                enterprise_latitude = float(enterprise.latitude)
                enterprise_longitude = float(enterprise.longitude)

                distance = self.calulate_distance(
                    user_latitude=lat,
                    user_longitude=lng,
                    enterprise_latitude=enterprise_latitude,
                    enterprise_longitude=enterprise_longitude,
                )

                if distance <= target:
                    near_enterprises.append(enterprise)

        near_enterprises_count = sum(1 for el in near_enterprises if el.type == "1")
        near_technicians_count = sum(1 for el in near_enterprises if el.type == "2")

        return near_enterprises, near_enterprises_count, near_technicians_count

    def calulate_distance(self, **kwargs):
        distance = self.common_service.calculate_semiversen(
            user_latitude=kwargs.get("user_latitude"),
            user_longitude=kwargs.get("user_longitude"),
            enterprise_latitude=kwargs.get("enterprise_latitude"),
            enterprise_longitude=kwargs.get("enterprise_longitude"),
        )
        
        return distance
