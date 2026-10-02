
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

#1. Motor de conexión
engine = create_async_engine(
    settings.DATABASE_URL,
    echo = False
)

#2. Fabricar sesiones
AsyncSessionLocal = async_sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush = False,
    expire_on_commit = False,
    class_ = AsyncSession
)

#3. Clase base
class Base(DeclarativeBase):
    pass

#4. Generador de sesiones para las peticiones HTTP
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session