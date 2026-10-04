from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.entities import TrainingDays, AttendanceStatus

#1. usuarios y autenticación

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime
    
    model_config = ConfigDict(from_attributes = True)
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
    
#2 equipos

class TeamBase(BaseModel):
    name: str
    training_days: TrainingDays = TrainingDays.martes_jueves

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: str
    
    model_config = ConfigDict(from_attributes = True)


#3. Jugadores

class PlayerBase(BaseModel):
    name: str
    
class PlayerCreate(PlayerBase):
    team_id: str
    
class PlayerResponse(PlayerBase):
    id: str
    team_id: str
    
    model_config = ConfigDict(from_attributes = True)
    
#4. Asistencia

class AttendanceBase(BaseModel):
    player_id: str
    date: str
    status: AttendanceStatus
    
class AttendanceCreate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    id:str
    
    model_config = ConfigDict(from_attributes = True)
    
#5. Estado completo

class DataStateResponse(AttendanceBase):
    teams:  List[TeamResponse]
    player: List[PlayerResponse]
    attendances: List[AttendanceResponse]
    
    model_config = ConfigDict(from_attributes = True)
    
class AddCoachRequest(BaseModel):
    team_id: str
    coach_email: str