from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db import connections
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .throttles import CornRateThrottle
from .utils import get_client_ip
from .services import CornService



class BuyCornView(APIView):
    """
    Endpoint para comprar maíz.
    Aplica la restricción de 1 maíz por minuto (CornRateThrottle).
    """

    throttle_classes = [CornRateThrottle]

    @extend_schema(
        summary="Comprar Maíz 🌽",
        description="Endpoint principal para registrar una compra. Identifica al usuario por IP y aplica un límite estricto de 1 compra por minuto.",
        responses={
            200: OpenApiTypes.OBJECT,
            429: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Compra Exitosa",
                value={"message": "¡Disfruta tu maíz! 🌽", "total_corn": 42},
                response_only=True,
                status_codes=[200],
            ),
            OpenApiExample(
                "Bloqueo por Rate Limit",
                value={
                    "detail": "Request was throttled. Expected available in 60 seconds."
                },
                response_only=True,
                status_codes=[429],
            ),
        ],
    )
    def post(self, request: Request) -> Response:
        ip: str = get_client_ip(request)

        new_total: int = CornService.process_purchase(ip)

        return Response({"message": "¡Disfruta tu maíz! 🌽", "total_corn": new_total})


class HealthCheckView(APIView):
    """
    Endpoint simple para verificar que el servicio está arriba.
    """

    authentication_classes = []
    permission_classes = []

    # @extend_schema(exclude=True)
    def get(self, request: Request) -> Response:
        health_status = {"status": "ok", "components": {}}
        
        # 1. Verificar DB
        try:
            connections['default'].cursor()
            health_status["components"]["db"] = "healthy"
        except Exception:
            health_status["components"]["db"] = "unhealthy"
            health_status["status"] = "error"

        # 2. Verificar Caché (Redis)
        try:
            cache.set("health_check", "ok", 1)
            if cache.get("health_check") == "ok":
                health_status["components"]["cache"] = "healthy"
            else:
                raise Exception("Cache write failed")
        except Exception:
            health_status["components"]["cache"] = "unhealthy"
            health_status["status"] = "error"

        status_code = 200 if health_status["status"] == "ok" else 503
        return Response(health_status, status=status_code)


def index(request: HttpRequest) -> HttpResponse:
    """
    Vista que renderiza el frontend e inyecta el contador inicial.
    """
    ip = get_client_ip(request)

    initial_count = CornService.get_corn_count(ip)

    return render(request, "core/index.html", {"initial_count": initial_count})
