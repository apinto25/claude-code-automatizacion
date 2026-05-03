# Appointments API

## Sobre este repositorio

Este repositorio forma parte del curso de LinkedIn Learning **Claude Code: Automatización del desarrollo de software**. El curso enseña a usar Claude Code como asistente de desarrollo de software: cómo interactuar con él para explorar código, hacer preguntas, recibir sugerencias y trabajar de forma más eficiente en el día a día como desarrollador.

---

## Descripción general

La API permite crear, consultar, actualizar y eliminar citas. Cada cita tiene un título, una descripción y ubicación opcionales, una fecha y hora programada, y un estado (`pending`, `confirmed` o `cancelled`).

El proyecto está estructurado para ser fácilmente extensible — versiones futuras agregarán campos como `created_at`, `duration` y un módulo de notificaciones.

### Stack

- **FastAPI** — framework web
- **SQLAlchemy** — ORM
- **SQLite** — base de datos (basada en archivo, sin configuración adicional)
- **Pydantic v2** — validación de peticiones y respuestas
- **uv** — gestor de paquetes

### Estructura del proyecto

```
appointments-api/
├── app/
│   ├── main.py           # Punto de entrada, inicialización de la BD
│   ├── database.py       # Engine, sesión, Base, dependencia get_db
│   ├── models/           # Modelos de SQLAlchemy
│   ├── schemas/          # Esquemas de Pydantic
│   ├── crud/             # Operaciones con la base de datos
│   └── routers/          # Manejadores de rutas
└── tests/
```

## Cómo ejecutar el proyecto

**Prerequisito:** tener [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado.

```bash
# Instalar dependencias
uv sync

# Iniciar el servidor de desarrollo
uv run uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`.  
Documentación interactiva (Swagger UI) en `http://127.0.0.1:8000/docs`.

## Endpoints

| Método   | Ruta                     | Descripción               |
|----------|--------------------------|---------------------------|
| `GET`    | `/appointments/`         | Listar todas las citas    |
| `GET`    | `/appointments/{id}`     | Obtener una cita          |
| `POST`   | `/appointments/`         | Crear una cita            |
| `PATCH`  | `/appointments/{id}`     | Actualización parcial     |
| `DELETE` | `/appointments/{id}`     | Eliminar una cita         |

### Ejemplo de petición

```bash
curl -X POST http://127.0.0.1:8000/appointments/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sincronización de equipo",
    "scheduled_at": "2026-05-10T10:00:00",
    "location": "Sala 3B",
    "status": "confirmed"
  }'
```
