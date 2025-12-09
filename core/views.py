from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction
from .throttles import CornRateThrottle

class BuyCornView(APIView):
    """
    Endpoint para comprar maíz.
    Aplica la restricción de 1 maíz por minuto (CornRateThrottle).
    """
    throttle_classes = [CornRateThrottle]

    def post(self, request):
        # 1. Obtener la IP del cliente de forma robusta
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # 2. Registrar la transacción
        # Si la ejecución llega a esta línea, significa que el Throttle permitió el paso.
        # Si no, DRF hubiera lanzado automáticamente un error 429.
        Transaction.objects.create(client_ip=ip)

        # 3. Contar cuánto maíz ha comprado este cliente en total
        total_corn = Transaction.objects.filter(client_ip=ip).count()

        return Response({
            "message": "Enjoy your corn! 🌽",
            "total_corn": total_corn
        })