from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, verify_team_coach
from app.db.session import get_db
from app.ia.client import get_embedded_text
from app.models.entities import Note, Player, User
from app.schemas.schemas import NoteCreate, NoteResponse

router = APIRouter(prefix="/notes", tags=["Notas"])

@router.post("/player/{player_id}", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_player_note(
    player_id: str,
    note_in: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    player_query = await db.execute(select(Player).where(Player.id == player_id))
    player = player_query.scalar_one_or_none()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jugador no encontrado"
        )

    await verify_team_coach(player.team_id, current_user.id, db)
    
    embedded_text = await get_embedded_text(note_in.content)
    
    new_note = Note(
        player_id=player_id,
        content=note_in.content,
        embedding=embedded_text
    )

    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)

    return new_note


@router.get("/player/{player_id}", response_model=List[NoteResponse])
async def list_player_notes(
    player_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    player_query = await db.execute(select(Player).where(Player.id == player_id))
    player = player_query.scalar_one_or_none()

    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jugador no encontrado"
        )

    await verify_team_coach(player.team_id, current_user.id, db)

    result = await db.execute(
        select(Note)
        .where(Note.player_id == player_id)
        .order_by(Note.created_at.desc())
    )
    notes = result.scalars().all()

    return notes
