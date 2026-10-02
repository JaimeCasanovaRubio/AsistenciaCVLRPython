
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.core.security import decode_access_token
from app.models.entities import User,Team

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "/api/auth/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
)-> User:
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "No se han podido validar las credenciales de la cuenta",
        headers = {"WWW-Authenticate": "Bearer"}, 
    )
    
    payload = decode_access_token(token)
    if payload is None: 
        print("no se saco el token")
        raise credentials_exception
    
    user_id: str | None = payload.get("sub")
    if user_id is None:
        print("no existe user_id en el token")
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        print("no existe el usuario en bbdd")
        raise credentials_exception
    
    return user

async def verify_team_coach(team_id: str, user_id: str, db: AsyncSession) ->Team:
    #comprueba que el equipo exista y si el entrenador es de ese equipo
    
    result = await db.execute(select(Team).join(Team.coaches).where(Team.id == team_id, User.id == user_id))
    team = result.scalar_one_or_none()
    
    if not team:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "El equipo no existe o no eres su entrenador"
        )
    
    return team