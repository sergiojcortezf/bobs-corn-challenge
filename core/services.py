from .models import Transaction

class CornService:
    @staticmethod
    def process_purchase(client_ip: str) -> int:
        """
        Ejecuta la lógica de negocio para una compra de maíz.
        1. Registra la transacción.
        2. Retorna el nuevo total de maíz del cliente.
        """
        Transaction.objects.create(client_ip=client_ip)
        
        return Transaction.get_count_for_ip(client_ip)