from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from rest_framework.test import APIClient
from rest_framework import status
from .models import Transaction


class BuyCornTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("buy-corn")

    def tearDown(self):
        cache.clear()

    def test_buy_corn_success(self):
        """
        Prueba que un usuario puede comprar una mazorca exitosamente.
        """
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "¡Disfruta tu maíz! 🌽")
        self.assertEqual(Transaction.objects.count(), 1)

    def test_rate_limit_blocking(self):
        """
        Prueba que el sistema bloquea al usuario si intenta comprar
        dos veces en menos de un minuto.
        """
        response1 = self.client.post(self.url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        response2 = self.client.post(self.url)
        self.assertEqual(response2.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        self.assertEqual(Transaction.objects.count(), 1)
