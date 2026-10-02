from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import jwt
from pwdlib import PasswordHash

from app.core.config import settings

#gestor de contraseñas con argon2

password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    #comprueba la contraseña con el hash de la bbdd
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password: str)-> str:
    #convierte al contraseña en un hash
    return password_hash.hash(password)

def create_access_token(subject: str, expires_delta: Optional[timedelta]= None)-> str:
    #genera token jwt firmado
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = settings.ACCES_TOKEN_EXPIRE_MINUTES)
    
    to_encode: dict[str, any] = {
        "sub": str(subject),
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token : str)-> Optional[dict[str,any]]:
    #comprueba el token
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms = [settings.ALGORITHM])
        return payload
    except jwt.PyJWKError:
        return None
    
    
    
    
    
    