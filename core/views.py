from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
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

    def post(self, request):
        ip = get_client_ip(request)

        new_total = CornService.process_purchase(ip)

        return Response({
            "message": "¡Disfruta tu maíz! 🌽",
            "total_corn": new_total
        })


def index(request):
    """
    Vista que renderiza el frontend e inyecta el contador inicial.
    """
    ip = get_client_ip(request)

    initial_count = Transaction.get_count_for_ip(ip)

    # 3. Pasar el dato al HTML
    return render(request, "core/index.html", {"initial_count": initial_count})
