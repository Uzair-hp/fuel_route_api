import numpy as np
import polyline

from .fuel_loader import fuel_service


class FuelOptimizer:
    def __init__(self):
        self.mpg = 10
        self.max_range = 500
        self.safety_margin = 500
        self.fuel_data = fuel_service.get_fuel_data()

    @staticmethod
    def haversine_distance(lat1, lon1, lats, lons):
        radius_miles = 3958.8
        lat1, lon1, lats, lons = map(np.radians, [lat1, lon1, lats, lons])
        dlat = lats - lat1
        dlon = lons - lon1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lats) * np.sin(dlon / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))
        return radius_miles * c

    def find_cheapest_nearest_station(self, lat, lon, radius=20):
        df = self.fuel_data.copy()
        if df.empty:
            return None

        df["dist_to_point"] = self.haversine_distance(
            lat,
            lon,
            df["latitude"].values,
            df["longitude"].values,
        )
        nearby_stations = df[df["dist_to_point"] <= radius]
        if nearby_stations.empty:
            return None

        cheapest = nearby_stations.sort_values("Retail Price").iloc[0]
        return {
            "name": cheapest["Truckstop Name"],
            "address": cheapest["Address"],
            "city": cheapest["City"],
            "state": cheapest["State"],
            "price": float(cheapest["Retail Price"]),
            "lat": float(cheapest["latitude"]),
            "lon": float(cheapest["longitude"]),
        }

    def calculate_stops(self, route_geometry, total_distance):
        points = polyline.decode(route_geometry)
        stops = []
        distance_since_last_fill = 0.0
        total_fuel_cost = 0.0

        for i in range(1, len(points)):
            prev_point = points[i - 1]
            curr_point = points[i]
            segment_dist = float(
                self.haversine_distance(
                    prev_point[0], prev_point[1], curr_point[0], curr_point[1]
                )
            )
            distance_since_last_fill += segment_dist

            if distance_since_last_fill >= self.safety_margin:
                station = self.find_cheapest_nearest_station(curr_point[0], curr_point[1])
                if station:
                    stops.append(station)
                    gallons_needed = distance_since_last_fill / self.mpg
                    total_fuel_cost += gallons_needed * station["price"]
                    distance_since_last_fill = 0.0

        if distance_since_last_fill > 0:
            fallback_station = (
                stops[-1]
                if stops
                else self.find_cheapest_nearest_station(points[-1][0], points[-1][1])
            )
            if fallback_station:
                gallons_needed = distance_since_last_fill / self.mpg
                total_fuel_cost += gallons_needed * fallback_station["price"]

        return stops, total_fuel_cost
