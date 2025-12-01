from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Snake Game API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"  # TODO: Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    # For PostgreSQL: postgresql://user:password@host:port/dbname
    #   Local development: postgresql://your_username@localhost:5432/snake_game
    #   Docker: postgresql://postgres:postgres@postgres:5432/snake_game
    # For SQLite: sqlite:///./snake_game.db
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/snake_game"
    
    # Session timeout in seconds (default 5 minutes)
    SESSION_TIMEOUT: int = 300
    
    # CORS settings
    # For development, use "*" to allow all origins
    # For production, specify exact origins: "https://yourdomain.com,https://www.yourdomain.com"
    CORS_ORIGINS: str = "*"  # Allow all origins for development
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
