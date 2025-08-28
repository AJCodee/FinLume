from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
   
    # auth/jwt
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        
settings = Settings()