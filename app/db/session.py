
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Comprueba si la conexión sigue viva antes de usarla
    pool_recycle=300,    # Recicla conexiones tras 5 min de inactividad
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

#3. Clase base
class Base(DeclarativeBase):
    pass

#4. Generador de sesiones para las peticiones HTTP
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        

