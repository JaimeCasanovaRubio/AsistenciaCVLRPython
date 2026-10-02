from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.api.deps import get_current_user, verify_team_coach
from app.models.entities import User, Team, Player
from app.schemas.schemas import PlayerCreate, PlayerResponse

router = APIRouter(prefix = "/player", tags = ["Jugadores"])



@router.post("", response_model = PlayerResponse, status_code = status.HTTP_201_CREATED)
async def create_player(
    player_in: PlayerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):  
    #crea un jugador y lo vincula a un equipo del entrenador
    await verify_team_coach(player_in.team_id, current_user.id, db)
    
    new_player = Player(
        name = player_in.name,
        team_id = player_in.team_id,
    )  
    
    db.add(new_player)
    await db.commit()
    await db.refresh(new_player)
    
    return new_player

@router.get("/team/{team_id}", response_model= List[PlayerResponse])
async def list_player_by_team(
    team_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    #obtiene el equipo completo
    await verify_team_coach(team_id, current_user.id, db)
    
    result = await db.execute(select(Player).where(Player.team_id == team_id))
    players = result.scalars().all()
    
    return players