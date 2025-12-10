# Especificación de Requisitos y Arquitectura: Bob's Corn Shop

**Autor:** Sergio Cortez  
**Rol:** Ingeniero de Software  
**Fecha:** Diciembre, 2025

---

## 1. Introducción

### 1.1 Propósito

Este documento define los requisitos funcionales, no funcionales y la arquitectura de software para el sistema "Bob's Corn Shop". El objetivo es proveer una solución tecnológica escalable para gestionar la venta equitativa de maíz bajo alta demanda.

### 1.2 Alcance

El sistema abarca una API RESTful para el procesamiento de compras y una interfaz de usuario web (Cliente Portal) y un panel administrativo de auditoría. Incluye mecanismos de defensa contra abuso (Rate Limiting) y persistencia de datos.

---

## 2. Descripción General

Bob requiere un mecanismo para controlar la demanda de su producto, estableciendo una política de "Fair Use" (Uso Justo) donde cada cliente solo puede adquirir una unidad de producto por minuto, identificado por su dirección de red.

---

## 3. Requerimientos Funcionales (RF)

_Acciones específicas que el sistema debe ser capaz de realizar._

**Módulo de Ventas (Backend)**

- **RF-01 Procesamiento de Transacción:** El sistema debe permitir recibir solicitudes de compra vía HTTP POST.
- **RF-02 Validación de Regla de Negocio (Rate Limiting):** El sistema debe validar que el cliente no haya realizado una compra en los últimos 60 segundos.
- **RF-03 Registro de Transacción:** El sistema debe persistir cada venta exitosa en base de datos relacional para auditoría.
- **RF-04 Respuesta de Bloqueo:** En caso de violar la regla RF-02, el sistema debe rechazar la solicitud con un código HTTP `429 Too Many Requests` e incluir el tiempo de espera restante en los headers (`Retry-After`).
- **RF-05 Monitoreo de Salud:** El sistema debe exponer un endpoint público (`/health/`) que responda con un estado `200 OK` y metadatos básicos para permitir verificaciones de disponibilidad (Health Checks) por orquestadores como Kubernetes o AWS Load Balancers.

**Módulo de Cliente (Frontend)**

- **RF-06 Interfaz de Compra:** Interfaz gráfica simple que permita iniciar una transacción.
- **RF-07 Visualización de Inventario:** Mostrar al usuario la cantidad total adquirida en tiempo real.
- **RF-08 Feedback Visual:** Notificar visualmente el éxito o bloqueo. En caso de bloqueo, mostrar un cronómetro con el tiempo de espera restante.

---

## 4. Requerimientos No Funcionales (RNF)

_Atributos de calidad del sistema._

- **RNF-01 Usabilidad:** La interfaz debe ser intuitiva (menos de 2 clicks para comprar) y responsiva (Mobile-first).
- **RNF-02 Portabilidad:** El sistema debe ser agnóstico al entorno, desplegable vía contenedores (Docker).
- **RNF-03 Resiliencia:** El sistema de Rate Limit debe persistir sus datos incluso si el servidor de aplicación se reinicia.
- **RNF-04 Mantenibilidad:** El código debe seguir principios SOLID y separar responsabilidades (Service Layer Pattern).
- **RNF-05 Observabilidad:** El sistema debe generar logs estructurados de cada transacción exitosa o error crítico para facilitar el monitoreo y depuración.
- **RNF-06 Integridad Continua:** Cada cambio en el código fuente (`push`) debe disparar una batería de pruebas automatizadas en un entorno limpio para garantizar la estabilidad del sistema antes de cualquier despliegue.

---

## 5. Restricciones Técnicas (Tech Stack)

_Tecnologías y herramientas obligatorias para la implementación._

- **Lenguaje:** Python 3.11+
- **Framework:** Django 4.x + DRF
- **Base de Datos:** SQLite (Relacional/Transaccional)
- **Caché:** Redis 7 (NoSQL/Key-Value para Throttling)
- **Frontend:** HTML5 + JS (Vanilla) + TailwindCSS
- **Infraestructura:** Docker Compose

---

## 6. Arquitectura del Sistema

### 6.1 Diagrama Conceptual

El sistema sigue una arquitectura por capas. La petición pasa por un filtro de caché antes de tocar la lógica de negocio o la base de datos principal.

`Cliente` --> `Vista (API View)` --> **`Redis (Rate Limit Check)`** --> `Service Layer` --> `SQLite (Persistencia)`

### 6.2 Decisiones de Diseño y Justificación

1.  **Rate Limiting Distribuido (Redis):**

    - _Decisión:_ Uso de **Redis** como backend de caché principal.
    - _Justificación:_ A diferencia de la memoria local, Redis permite que el estado del bloqueo persista entre reinicios del servidor y sea compartido si escalamos a múltiples instancias (workers) de Django en el futuro.
    - _Fallback:_ Se implementó una lógica condicional (`USE_REDIS`) para permitir el desarrollo local sin dependencias fuertes.

2.  **Patrón Service Layer (Capa de Servicio):**

    - _Decisión:_ Extracción de la lógica de negocio a `core/services.py`.
    - _Justificación:_ Aplicación del Principio de Responsabilidad Única (SRP). La Vista (`views.py`) solo gestiona la petición HTTP y la serialización; el Servicio gestiona las reglas del negocio. Esto facilita la creación de pruebas unitarias aisladas y futuros cambios en la lógica.

3.  **Identificación por IP:**

    - _Contexto:_ No existe requerimiento de autenticación/login.
    - _Decisión:_ Se utiliza la IP del request. Se implementó una utilidad (`utils.py`) para extraer la IP real incluso detrás de proxies (`HTTP_X_FORWARDED_FOR`).

4.  **Frontend Ligero (No-Build):**

    - _Decisión:_ Uso de Tailwind vía CDN y JS Vanilla.
    - _Justificación:_ Elimina la complejidad de un pipeline de construcción (Webpack/Vite) para este MVP, permitiendo un despliegue monolítico simple y rápido.

5.  **Auditoría y Seguridad (Admin Panel):**

    - _Decisión:_ Habilitación del Django Admin en modo _Read-Only_.
    - _Justificación:_ Provee una interfaz inmediata para que los stakeholders (Bob) revisen las ventas sin riesgo de manipular o borrar la data histórica (Integridad de Datos).

6.  **Automatización de Pruebas (CI):**
    - _Decisión:_ Implementación de un pipeline de GitHub Actions (`.github/workflows/ci.yml`).
    - _Justificación:_ Elimina el error humano en la verificación de calidad. Asegura que la lógica crítica (Rate Limit) y la integración de las vistas funcionen correctamente en cada iteración del desarrollo.

---

## 7. Suposiciones y Limitaciones

- Se asume que SQLite es suficiente para la persistencia transaccional del MVP.
- La seguridad se basa en IP; usuarios bajo una misma NAT (ej. oficinas) compartirán el límite de compra.
