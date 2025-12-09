from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction
from .throttles import CornRateThrottle
from .utils import get_client_ip

class BuyCornView(APIView):
    """
    Endpoint para comprar maíz.
    Aplica la restricción de 1 maíz por minuto (CornRateThrottle).
    """
    throttle_classes = [CornRateThrottle]

    def post(self, request):
        
        ip = get_client_ip(request)

        # Lógica de negocio
        Transaction.objects.create(client_ip=ip)

        total_corn = Transaction.get_count_for_ip(ip)

        return Response({
            "message": "Enjoy your corn! 🌽",
            "total_corn": total_corn
        })


def index(request):
    """
    Vista que renderiza el frontend e inyecta el contador inicial.
    """
    ip = get_client_ip(request)

    initial_count = Transaction.get_count_for_ip(ip)

    # 3. Pasar el dato al HTML
    return render(request, 'core/index.html', {'initial_count': initial_count})