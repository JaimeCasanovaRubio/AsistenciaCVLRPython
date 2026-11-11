# Asistencia CVLR

API backend para gestionar equipos, jugadores, asistencias y observaciones de jugadores.

Este proyecto está pensado para servir de base para una aplicación de entrenamiento o control de asistencia deportiva, con autenticación de entrenadores y permisos por equipo.

## Tecnologías

- Python
- FastAPI
- SQLAlchemy (async)
- Pydantic
- PostgreSQL / base de datos configurada por variable de entorno
- JWT para autenticación

## Estructura del proyecto

```text
app/
  api/
    deps.py
    routes/
      auth.py
      teams.py
      players.py
      attendances.py
      notes.py
  core/
    config.py
    security.py
  db/
    session.py
  models/
    entities.py
  schemas/
    schemas.py
  main.py
requirements.txt
README.md
```

## Objetivo del backend

La API permite:

- registrar entrenadores/usuarios
- crear equipos
- asociar entrenadores a equipos
- crear jugadores dentro de equipos
- registrar asistencias por jugador y fecha
- guardar observaciones/notas por jugador
- proteger las rutas por autenticación y por pertenencia al equipo

## Arquitectura general

El proyecto sigue una estructura simple por capas:

- `app/models/entities.py`: modelos SQLAlchemy
- `app/schemas/schemas.py`: validación de entrada y salida
- `app/api/routes`: endpoints HTTP
- `app/api/deps.py`: dependencias comunes, autenticación y control de permisos
- `app/db/session.py`: acceso a la base de datos

## Configuración inicial

1. Crear un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Crear un archivo `.env` en la raíz del proyecto con este formato:

```env
DATABASE_URL=postgresql+asyncpg://usuario:password@localhost:5432/asistenciacvlr
SECRET_KEY=tu_clave_secreta_muy_segura
ALGORITHM=HS256
```

> Si usas otra base de datos, ajusta `DATABASE_URL` según tu motor y driver.

## Arranque del proyecto

Ejecuta la API con:

```bash
uvicorn app.main:app --reload
```

La API quedará disponible normalmente en:

```text
http://localhost:8000
```

La documentación automática de FastAPI estará en:

```text
http://localhost:8000/docs
```

## Autenticación

La autenticación está basada en JWT.

Se utilizan dos endpoints principales:

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/token`

La respuesta incluye un token JWT que después se envía en el header:

```http
Authorization: Bearer <token>
```

## Endpoints principales

### Autenticación

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/token`

### Equipos

- `POST /api/teams`
- `GET /api/teams`
- `POST /api/teams/{team_id}/coaches`

### Jugadores

- `POST /api/player`
- `GET /api/player/team/{team_id}`

### Asistencias

- `GET /api/teams/{team_id}/attendances`
- `POST /api/attendance`

### Notas

Se recomienda mantener la lógica separada por jugador, por ejemplo:

- `POST /api/notes/player/{player_id}`
- `GET /api/notes/player/{player_id}`

Esto permite que la UI maneje el menú de cada jugador sin mezclar la nota en el objeto del jugador.

## Permisos y seguridad

La validación se hace con la dependencia `verify_team_coach`.

Esto asegura que:

- un usuario solo pueda gestionar equipos en los que sea entrenador
- no pueda modificar datos de equipos ajenos
- no pueda crear asistencias o notas para jugadores fuera de su equipo

## Modelo conceptual

Las entidades principales son:

- `User`: entrenador o usuario autenticado
- `Team`: equipo deportivo
- `Player`: jugador dentro de un equipo
- `Attendance`: registro de asistencia con fecha y estado
- `Note`: observación textual asociada a un jugador

## Recomendaciones

- Mantener la separación de responsabilidades:
  - `players.py` para jugadores
  - `notes.py` para observaciones
  - `attendances.py` para asistencia
- No mezclar dentro del modelo del jugador una lista de notas si la idea es gestionarlas como recurso independiente.
- Usar siempre un token JWT en rutas protegidas.
- Mantener `.env` fuera del repositorio si no quieres compartir secretos.

## Estado

Este proyecto está en una etapa de backend funcional y estructurado, ideal para continuar ampliando funcionalidades o conectarlo con un frontend.

## Siguientes pasos sugeridos

- añadir paginación en listados
- añadir edición y borrado de notas
- añadir búsqueda por jugador o fecha
- añadir más validaciones de negocio
- conectar con una app frontend en React, Vue o Flutter

## Nota

Este README sirve como guía de arranque y entendimiento del proyecto. Si vuelves a retomarlo después de un tiempo, lo más importante es seguir esta regla:

- jugadores, equipos, asistencias y notas son recursos separados
- cada recurso tiene su propio router y su propio esquema
- la autenticación y permisos se resuelven por equipo
