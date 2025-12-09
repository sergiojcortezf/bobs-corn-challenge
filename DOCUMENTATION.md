# Especificación de Requisitos y Arquitectura: Bob's Corn Shop

**Autor:** Sergio Cortez  
**Rol:** Ingeniero de Software  
**Fecha:** 9 de Diciembre, 2025

---

## 1. Introducción

### 1.1 Propósito

Este documento define los requisitos funcionales y no funcionales, así como la arquitectura de software para el sistema "Bob's Corn Shop". El objetivo es proveer una solución tecnológica para gestionar la venta equitativa de maíz.

### 1.2 Alcance

El sistema abarca una API RESTful para el procesamiento de compras y una interfaz de usuario web (Cliente Portal) para la interacción con el usuario final. El sistema se limita a ventas anónimas identificadas por red.

---

## 2. Descripción General

Bob requiere un mecanismo para controlar la demanda de su producto, estableciendo una política de "Fair Use" (Uso Justo) donde cada cliente solo puede adquirir una unidad de producto por minuto.

---

## 3. Requerimientos Funcionales (RF)

_Acciones específicas que el sistema debe ser capaz de realizar._

**Módulo de Ventas (Backend)**

- **RF-01 Procesamiento de Transacción:** El sistema debe permitir recibir solicitudes de compra mediante un protocolo HTTP.
- **RF-02 Validación de Regla de Negocio (Rate Limiting):** El sistema debe validar que el origen de la solicitud (Cliente) no haya realizado una compra exitosa en los últimos 60 segundos.
- **RF-03 Registro de Transacción:** El sistema debe persistir los datos de cada venta exitosa (Fecha, Hora, Identificador del Cliente) para fines de auditoría e inventario.
- **RF-04 Respuesta de Bloqueo:** En caso de violar la regla de negocio (RF-02), el sistema debe rechazar la solicitud retornando un código de estado HTTP estándar para "Demasiadas Solicitudes".

**Módulo de Cliente (Frontend)**

- **RF-05 Interfaz de Compra:** El sistema debe proveer una interfaz gráfica que permita al usuario iniciar una transacción con un solo click.
- **RF-06 Visualización de Inventario Personal:** El sistema debe mostrar al usuario la cantidad total de unidades adquiridas exitosamente en la sesión actual.
- **RF-07 Feedback de Estado:** El sistema debe notificar visualmente al usuario el resultado de su intento de compra (Éxito o Bloqueo Temporal).

---

## 4. Requerimientos No Funcionales (RNF)

_Atributos de calidad del sistema._

- **RNF-01 Usabilidad:** La interfaz de usuario debe ser intuitiva para personas sin conocimientos técnicos (Criterio: Menos de 2 clicks para realizar una compra).
- **RNF-02 Portabilidad:** El sistema debe ser capaz de desplegarse en cualquier entorno compatible con contenedores (Docker) sin configuración manual compleja.
- **RNF-03 Mantenibilidad:** El código debe seguir los estándares PEP-8 (Python) y principios de diseño modular para facilitar futuras integraciones (ej. Autenticación real).
- **RNF-04 Rendimiento:** El tiempo de respuesta de la API para la validación de la compra no debe exceder los 200ms bajo carga normal.

---

## 5. Restricciones Técnicas (Tech Stack)

_Tecnologías y herramientas obligatorias para la implementación._

- **Lenguaje:** Python 3.11+
- **Framework Backend:** Django 4.x + Django REST Framework (DRF)
- **Base de Datos:** SQLite (Entorno de Desarrollo/Prueba)
- **Frontend:** HTML5 + JavaScript (Vanilla) + TailwindCSS (CDN)
- **Infraestructura:** Docker & Docker Compose

---

## 6. Arquitectura del Sistema

### 6.1 Diagrama Conceptual

El sistema sigue una arquitectura monolítica modular. Django sirve tanto los recursos estáticos (HTML templates) como los endpoints de la API JSON.

`Cliente (Navegador)` <--> `Proxy Inverso / Servidor Web (Django Dev Server)` <--> `Vista (DRF + Lógica)` <--> `Base de Datos (SQLite)`

### 6.2 Decisiones de Diseño y Justificación

1.  **Identificación por IP (Throttling):**

    - _Contexto:_ No existe requerimiento de Login.
    - _Decisión:_ Se utiliza la clase `AnonRateThrottle` de DRF mapeada a la dirección IP del request.
    - _Trade-off:_ Usuarios bajo una misma NAT compartirán el límite. Se acepta para el MVP.

2.  **Inyección de Dependencias (Frontend):**

    - _Decisión:_ Uso de Tailwind vía CDN.
    - _Justificación:_ Elimina la necesidad de un paso de compilación (Build step) de Node.js, simplificando el despliegue a un solo contenedor Docker.

3.  **Manejo de Estado (Concurrencia):**
    - _Decisión:_ Uso del sistema de Caché de Django para el conteo de tiempo.
    - _Nota:_ En producción, el backend de caché debe configurarse con Redis para soportar múltiples instancias (workers).

---

## 7. Suposiciones y Limitaciones

- Se asume que la persistencia de datos local (SQLite) es suficiente para el alcance de la prueba.
- El sistema no maneja autenticación de usuarios; la seguridad se basa en la limitación por IP.
- No se implementa pasarela de pagos real.
