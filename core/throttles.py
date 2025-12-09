from rest_framework.throttling import AnonRateThrottle

class CornRateThrottle(AnonRateThrottle):
    """
    Limita a usuarios anónimos basándose en su IP.
    El 'scope' define la llave que buscaremos en settings.py.
    """
    scope = 'corn_purchase'