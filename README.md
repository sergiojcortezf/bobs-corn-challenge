# 🌽 Bob's Corn Shop

> Una solución Full-Stack robusta para la gestión equitativa de venta de maíz, construida con Django y Docker.

## 🚀 Características Principales

- **Rate Limiting Estricto:** Política de 1 compra/minuto por IP para evitar acaparamiento.
- **Arquitectura Limpia:** Lógica de negocio encapsulada y separada de las vistas.
- **Dockerized:** Despliegue agnóstico y rápido.
- **Testing:** Cobertura de pruebas unitarias para reglas de negocio críticas.
- **Frontend Moderno:** Interfaz reactiva con TailwindCSS y feedback visual inmediato.

## 🛠️ Stack Tecnológico

- **Backend:** Python 3.11, Django 4.2, Django REST Framework.
- **Frontend:** HTML5, JavaScript (Vanilla), TailwindCSS.
- **Infraestructura:** Docker Compose.
- **Docs:** OpenAPI (Swagger).

## ⚡ Inicio Rápido

1.  **Clonar y arrancar:**

    ```bash
    git clone <tu-repo>
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

## 📖 Documentación

Para detalles profundos sobre la arquitectura, decisiones de diseño y análisis de requerimientos, consulta el archivo [DOCUMENTATION.md](./DOCUMENTATION.md).

---

Hecho por **Sergio Cortez** para el reto técnico de Base Labs.
