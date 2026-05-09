from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RouteRequestSerializer
from .services.fuel_optimizer import FuelOptimizer
from .services.routing_service import RoutingService


def health_check(request):
    return JsonResponse({"status": "ok", "service": "fuel-route-api"})


class FuelRouteView(APIView):
    def post(self, request):
        serializer = RouteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start = serializer.validated_data["start"].strip()
        destination = serializer.validated_data["destination"].strip()

        cache_key = f"route::{start.lower()}::{destination.lower()}"
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return Response(cached_response)

        routing_service = RoutingService()
        optimizer = FuelOptimizer()

        start_coords = routing_service.get_coordinates(start)
        end_coords = routing_service.get_coordinates(destination)
        route_data = routing_service.get_route(start_coords, end_coords)

        stops, total_cost = optimizer.calculate_stops(
            route_data["geometry"],
            route_data["distance_miles"],
        )

        response_data = {
            "start": start,
            "destination": destination,
            "total_distance_miles": round(route_data["distance_miles"], 2),
            "estimated_gallons": round(route_data["distance_miles"] / optimizer.mpg, 2),
            "total_fuel_cost": round(total_cost, 2),
            "fuel_stops": stops,
            "route_geometry": route_data["geometry"],
        }

        cache.set(cache_key, response_data, 60 * 60 * 24)
        return Response(response_data)


