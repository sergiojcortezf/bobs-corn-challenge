from django.urls import path
from .views import BuyCornView, HealthCheckView

urlpatterns = [
    path("buy/", BuyCornView.as_view(), name="buy-corn"),
    path("health/", HealthCheckView.as_view(), name="health-check"),
]
