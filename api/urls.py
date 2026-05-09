from django.urls import path

from .views import FuelRouteView, health_check


urlpatterns = [
    path("", health_check, name="api-health"),
    path("optimize-route/", FuelRouteView.as_view(), name="optimize-route"),
]
