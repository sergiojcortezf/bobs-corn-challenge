from django.db import models
import uuid

class Transaction(models.Model):
    """
    Registra cada compra exitosa de maíz.
    Sirve para auditoría y para contar cuánto ha comprado un cliente.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_ip = models.GenericIPAddressField(db_index=True)
    amount = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_count_for_ip(cls, ip):
        return cls.objects.filter(client_ip=ip).count()

    def __str__(self):
        return f"{self.client_ip} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']