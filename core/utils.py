from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str | None:
    """
    Extrae la dirección IP del cliente de la solicitud HTTP.
    Soporta proxies mediante el encabezado X-Forwarded-For.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
