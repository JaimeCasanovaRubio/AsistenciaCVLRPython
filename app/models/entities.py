import enum
import uuid
from datetime import datetime
from typing import List
from sqlalchemy import String, DateTime, ForeignKey, Table, Column, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import  Base

def gen_id() -> str:
    #genera un id y lo retorna
    return uuid.uuid4().hex[:10]

#1. dias de entreno
class TrainingDays(str, enum.Enum):
    martes_jueves = "martes_jueves"
    lunes_miercoles = "lunes_miercoles"
    
#2. estados de asistencia
class AttendanceStatus(str, enum.Enum):
    asistido = "asistido"
    falta_justificada = "falta_justificada"
    falta_injustificada = "falta_injustificada"
    retraso = "retraso"
    
#3. tabla entre entrenadores y equipos
team_coaches = Table(
    "team_coaches",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("users.id", ondelete ="CASCADE"), primary_key = True),
    Column("team_id", String(36), ForeignKey("teams.id", ondelete ="CASCADE"), primary_key = True)
)

#4. entrenador/usuario
class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key = True, default = gen_id)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    email: Mapped[str] = mapped_column(String(255), unique = True, index = True, nullable = False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.utcnow)
    
    teams: Mapped[List["Team"]] = relationship(
        "Team",
        secondary = team_coaches,
        back_populates = "coaches"
    )
    
#5. equipos
class Team(Base):
    __tablename__ = "teams"
    id: Mapped[str] = mapped_column(String(36), primary_key = True, default = gen_id)
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    training_days: Mapped[TrainingDays] = mapped_column(
        Enum(TrainingDays, values_callable = lambda obj: [e.value for e in obj]),
        nullable = False,
        default = TrainingDays.martes_jueves
    )
    coaches: Mapped[List["User"]] = relationship(
        "User",
        secondary = team_coaches,
        back_populates = "teams"
    )
    players: Mapped[List["Player"]] = relationship(
        "Player",
        back_populates = "team",
        cascade = "all, delete-orphan"
    )
    
#6. jugador
class Player(Base):
    __tablename__ = "players"
    id: Mapped[str] = mapped_column(String(36), primary_key = True, default = gen_id)
    team_id: Mapped[str] = mapped_column(String(36), ForeignKey("teams.id", ondelete = "CASCADE"))
    name: Mapped[str] = mapped_column(String(100), nullable = False)
    
    team: Mapped["Team"] = relationship(
        "Team",
        back_populates = "players"
    )
    attendances: Mapped[List["Attendance"]] = relationship(
        "Attendance",
        back_populates = "player",
        cascade = "all, delete-orphan"
    )
    
    
#7. Asistencia
class Attendance(Base):
    __tablename__ = "attendances"
    id: Mapped[str] = mapped_column(String(36), primary_key = True, default = gen_id)
    player_id: Mapped[str] = mapped_column(String(36), ForeignKey("players.id", ondelete = "CASCADE"))
    date: Mapped[str] = mapped_column(String(10), nullable = False, index =  True)
    status: Mapped[AttendanceStatus] = mapped_column(
        Enum(AttendanceStatus, values_callable = lambda obj: [e.value for e in obj]),
        nullable = False,
        default = AttendanceStatus.asistido
    )
    
    player: Mapped["Player"] = relationship(
        "Player",
        back_populates = "attendances"
    )
    
    __table_args__ = (
        UniqueConstraint("player_id", "date", name = "uq_player_date_attendance"),
    )