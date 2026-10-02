from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.entities import User
from app.schemas.schemas import UserCreate, UserResponse, Token, LoginRequest
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings

router = APIRouter(prefix = "/auth", tags=["Autenticación"])


@router.post("/register", response_model = UserResponse, status_code = status.HTTP_201_CREATED)
async def register (
    user_in: UserCreate, 
    db: AsyncSession = Depends(get_db)
    ):
    #Registra a un nuevo entrenador tras verificar que el email sea único
    #1. comprobar si el email existe
    result = await db.execute(select(User).where(User.email ==user_in.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Ya existe un usuario con ese email",
        )
    
    #2. hashear la contraseña y crear la entidad
    new_user = User(
        name = user_in.name,
        email = user_in.email,
        password_hash = get_password_hash(user_in.password),
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


@router.post("/token", response_model = Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Correo o contraseña incorrecto",
            headers = {"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta (minutes = settings.ACCES_TOKEN_EXPIRE_MINUTES)
    acces_token = create_access_token(
        subject = user.id, expires_delta = access_token_expires
    )
    
    return Token(access_token = acces_token, token_type= "bearer")

@router.post("/login", response_model = Token)
async def login_json(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    #login mediante json
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "correo o contraseña incorrectos",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes = settings.ACCES_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject = user.id, expires_delta = access_token_expires
    )
    
    return Token(access_token= access_token, token_type = "bearer")