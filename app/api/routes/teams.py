
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.api.deps import get_current_user, verify_team_coach
from app.models.entities import User, Team
from app.schemas.schemas import TeamCreate, TeamResponse, AddCoachRequest

router = APIRouter(prefix = "/teams", tags = ["Equipos"])

@router.post("/create", response_model = TeamResponse, status_code = status.HTTP_201_CREATED)
async def create_team(
    team_in: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    #Crea un equipo y automaticamente le asigna el entrenador que sea el usuario
    new_team = Team(
        name = team_in.name,
        training_days = team_in.training_days,
    )
    new_team.coaches.append(current_user)
    
    db.add(new_team)
    await db.commit()
    await db.refresh(new_team)
    
    return new_team

@router.post("/add_coach", status_code = status.HTTP_202_ACCEPTED)
async def add_coach_to_team(
    data: AddCoachRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    team_id = data.team_id
    coach_email = data.coach_email
    # 1. Comprobar que el usuario actual tenga permisos sobre el equipo
    await verify_team_coach(team_id=team_id, user_id=current_user.id, db=db)

    # 2. Cargar el equipo precargando la relación 'coaches'
    result = await db.execute(
        select(Team)
        .options(selectinload(Team.coaches))
        .where(Team.id == team_id)
    )
    team = result.scalar_one_or_none()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipo no encontrado",
        )

    # 3. Comprobar si ya está asignado usando la relación que acabamos de cargar
    result = await db.execute(select(User.id).where(User.email == coach_email))
    new_coach_id = result.scalar_one_or_none()
    if any(coach.id == new_coach_id for coach in team.coaches):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este entrenador ya está asignado a este equipo",
        )

    # 4. Obtener y validar el nuevo entrenador
    res_coach = await db.execute(select(User).where(User.id == new_coach_id))
    new_coach = res_coach.scalar_one_or_none()
    if not new_coach:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe ese entrenador",
        )

    # 5. Añadir y persistir
    team.coaches.append(new_coach)
    await db.commit()
    await db.refresh(team)

    return team

@router.get("", response_model = List[TeamResponse])
async def list_my_teams(
    curren_user: User  = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    #devuelvev los equipos vinculados al entrenador
    result = await db.execute(
        select(Team).join(Team.coaches).where(User.id == curren_user.id)
    )
    teams = result.scalars().all()
    return teams


    