
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):   
    PROJECT_NAME: str = "AsistenciaCVLR"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCES_TOKEN_EXPIRE_MINUTES: int = 60*24*365*10
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore"
    )
        
settings = Settings()