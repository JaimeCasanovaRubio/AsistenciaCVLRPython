from fastapi import APIRouter, HTTPException, Depends, status
from datetime import date
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.api.deps import get_current_user, verify_team_coach
from app.models.entities import User, Team, Player, Attendance
from app.schemas.schemas import AttendanceCreate, AttendanceResponse

router = APIRouter(prefix = "/attendance", tags = ["Asistencias"])

@router.post("/bulk", status_code = status.HTTP_200_OK)
async def sumbit_bulk_attendance(
    attendance_data: AttendanceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Team.id).join(Team.players).where(Player.id == attendance_data.player_id))
    team_id = result.scalar_one_or_none()
    await verify_team_coach(team_id, current_user.id, db)
    
    new_attendance = Attendance(
        player_id = attendance_data.player_id,
        date = attendance_data.date,
        status = attendance_data.status,
    )
    
    db.add(new_attendance)
    await db.commit()
    await db.refresh(new_attendance)
    
    return new_attendance
    
