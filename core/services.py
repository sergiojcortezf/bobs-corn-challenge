import logging
from .models import Transaction

logger = logging.getLogger(__name__)


class CornService:
    @staticmethod
    def process_purchase(client_ip: str) -> int:
        """
        Ejecuta la lógica de negocio para una compra de maíz.
        1. Registra la transacción.
        2. Retorna el nuevo total de maíz del cliente.
        """
        try:
            Transaction.objects.create(client_ip=client_ip)
            new_total = Transaction.get_count_for_ip(client_ip)

            logger.info(
                f"Compra exitosa para IP: {client_ip}. Total actual: {new_total}"
            )
            return new_total

        except Exception as e:
            logger.error(f"Error procesando compra para {client_ip}: {str(e)}")
            raise e

    @staticmethod
    def get_corn_count(client_ip: str) -> int:
        """
        Simplemente consulta el saldo actual sin comprar nada.
        """
        return Transaction.get_count_for_ip(client_ip)
