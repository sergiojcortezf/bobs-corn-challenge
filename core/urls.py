from django.urls import path
from .views import BuyCornView

urlpatterns = [
    path("buy/", BuyCornView.as_view(), name="buy-corn"),
]
