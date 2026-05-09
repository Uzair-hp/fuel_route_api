import requests
from django.conf import settings


class RoutingService:
    def __init__(self):
        self.api_key = settings.ORS_API_KEY
        self.base_url = "https://api.openrouteservice.org"

    def _ensure_api_key(self):
        if not self.api_key:
            raise ValueError("ORS_API_KEY is not configured")

    def get_coordinates(self, location_name):
        self._ensure_api_key()
        url = f"{self.base_url}/geocode/search"
        params = {
            "api_key": self.api_key,
            "text": location_name,
            "boundary.country": "US",
            "size": 1,
        }
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if not data.get("features"):
            raise ValueError(f"Location not found: {location_name}")

        return data["features"][0]["geometry"]["coordinates"]

    def get_route(self, start_coords, end_coords):
        self._ensure_api_key()
        url = f"{self.base_url}/v2/directions/driving-car"
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        body = {
            "coordinates": [start_coords, end_coords],
            "instructions": False,
            "units": "mi",
        }
        response = requests.post(url, json=body, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        route = data["routes"][0]
        summary = route["summary"]
        distance = float(summary["distance"])

        return {
            "distance_miles": distance,
            "duration_seconds": float(summary["duration"]),
            "geometry": route["geometry"],
        }
