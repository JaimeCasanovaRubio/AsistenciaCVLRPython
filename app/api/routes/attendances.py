import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Ajusta las importaciones a tus rutas reales de modelos y dependencias
from app.db import get_db
from app.models import Attendance, Player, User
from app.schemas import AttendanceCreate, AttendanceResponse
from app.api.deps import get_current_user, verify_team_coach

router = APIRouter(tags=["Attendance"])


@router.get("/teams/{team_id}/attendances", response_model=List[AttendanceResponse])
async def get_team_attendances(
    team_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 1. Verificar que el usuario sea el entrenador del equipo
    await verify_team_coach(team_id, current_user.id, db)

    # 2. Obtener los IDs de todos los jugadores de ese equipo
    players_query = await db.execute(select(Player.id).where(Player.team_id == team_id))
    player_ids = players_query.scalars().all()

    if not player_ids:
        return []

    # 3. Obtener todas las asistencias asociadas a esos jugadores
    attendances_query = await db.execute(
        select(Attendance).where(Attendance.player_id.in_(player_ids))
    )
    attendances = attendances_query.scalars().all()

    return attendances


@router.post("/attendance", response_model=AttendanceResponse)
async def record_attendance(
    data: AttendanceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # 1. Comprobar que el jugador existe y obtener su team_id
    player_query = await db.execute(select(Player).where(Player.id == data.player_id))
    player = player_query.scalar_one_or_none()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jugador no encontrado"
        )

    # 2. Verificar que el usuario sea el entrenador del equipo del jugador
    await verify_team_coach(player.team_id, current_user.id, db)

    # 3. Comprobar si ya existe un registro de asistencia para este jugador y fecha
    existing_query = await db.execute(
        select(Attendance).where(
            Attendance.player_id == data.player_id,
            Attendance.date == data.date
        )
    )
    attendance_record = existing_query.scalar_one_or_none()

    if attendance_record:
        # Si ya existe, actualizamos el estado
        attendance_record.status = data.status
    else:
        # Si no existe, creamos un nuevo registro
        attendance_record = Attendance(
            id=str(uuid.uuid4())[:10],  # O el generador de IDs que uses
            player_id=data.player_id,
            date=data.date,
            status=data.status
        )
        db.add(attendance_record)

    await db.commit()
    await db.refresh(attendance_record)

    return attendance_record