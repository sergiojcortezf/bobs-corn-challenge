# 🌽 Bob's Corn Shop

![Bob's Corn CI](https://github.com/sergiojcortezf/bobs-corn-challenge/actions/workflows/ci.yml/badge.svg)

> Una solución Full-Stack robusta para la gestión equitativa de venta de maíz, construida con Django, Docker y Redis.

## 🚀 Características Principales

- **Rate Limiting Distribuido:** Política estricta de 1 compra/minuto por IP, gestionada con **Redis** para persistencia y soporte en entornos distribuidos.
- **Arquitectura por Capas:** Implementación del patrón **Service Layer** para desacoplar la lógica de negocio de las vistas (API), garantizando un código limpio y testeable.
- **Auditoría y Seguridad:** Panel de administración de solo lectura para auditar transacciones históricas.
- **Observabilidad:** Sistema de logging detallado para monitoreo de operaciones.
- **Resiliencia y Fallback:** Sistema inteligente que utiliza Redis si está disponible (Docker/Prod), pero hace fallback automático a memoria local para desarrollo simple.
- **Dockerized:** Despliegue agnóstico y rápido con orquestación de servicios.
- **Testing:** Cobertura de pruebas unitarias para reglas de negocio críticas.
- **Frontend Moderno:** Interfaz reactiva con TailwindCSS, manejo de estados de carga y feedback visual en tiempo real (cronómetro).

## 🛠️ Stack Tecnológico

- **Backend:** Python 3.11, Django 4.2, Django REST Framework.
- **Base de Datos:** SQLite (Persistencia de Transacciones).
- **Caché:** Redis 7 (Persistencia de Rate Limit).
- **Frontend:** HTML5, JavaScript (Vanilla), TailwindCSS via CDN.
- **Infraestructura:** Docker & Docker Compose.
- **DevOps:** GitHub Actions (CI/CD).
- **Documentación:** OpenAPI 3.0 (Swagger).

## ⚙️ Configuración y Variables de Entorno

El proyecto está diseñado bajo la metodología "12-Factor App". Requiere un archivo `.env` en la raíz, estas son las variables soportadas:

```ini
# --- SEGURIDAD ---
SECRET_KEY=django-insecure-tu-clave-secreta-aqui
DEBUG=1  # Poner en 0 para producción
ALLOWED_HOSTS=*

# --- ARQUITECTURA ---
# Controla si usamos Redis o Memoria Local para el Rate Limit.
# Ideal para entornos CI/CD donde no se quiere levantar un servicio Redis.
USE_REDIS=True
```

## ⚡ Inicio Rápido

1.  **Clonar y arrancar:**

    ```bash
    git clone https://github.com/sergiojcortezf/bobs-corn-challenge.git
    cd bobs-corn-challenge
    docker compose up --build
    ```

2.  **Acceder:**

    - 🏪 **Tienda:** [http://localhost:8000](http://localhost:8000)
    - 📘 **Documentación API:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

3.  **Correr Pruebas:**
    ```bash
    docker compose exec web python manage.py test core
    ```

> **Nota de Infraestructura:** La configuración actual de Docker Compose utiliza `python manage.py runserver` para facilitar la evaluación técnica. Para un despliegue en producción real, se recomienda sustituir este comando por un servidor WSGI robusto como **Gunicorn** o **Uvicorn** detrás de Nginx.

## 📖 Documentación

Para detalles profundos sobre la arquitectura, decisiones de diseño y análisis de requerimientos, consulta el archivo [DOCUMENTATION.md](./DOCUMENTATION.md).

---

Hecho por **Sergio Cortez** para el reto técnico de Base Labs.
