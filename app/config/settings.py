"""
Application configuration and settings management.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # ==================== API Configuration ====================
    app_name: str = "Portfolio AI Agent API"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"
    
    # ==================== Server Configuration ====================
    host: str = "0.0.0.0"
    port: int = 8000
    
    # ==================== CORS Configuration ====================
    # allowed_origins: Union[List[str], str] = "http://localhost:3000,http://127.0.0.1:3000"
    # allowed_origins: str = "http://localhost:3000"
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://howardye.up.railway.app",
        "https://portfolio-website-sigma-six-85.vercel.app"
    ]
    
    # def get_allowed_origins(self) -> List[str]:
    #     """Parse comma-separated ALLOWED_ORIGINS string into list."""
    #     print(f"🔍 RAW allowed_origins value: '{self.allowed_origins}'")
    #     print(f"🔍 Type: {type(self.allowed_origins)}")
        
    #     if not self.allowed_origins:
    #         return ["http://localhost:3000"]
        
    #     # Split by comma and strip whitespace
    #     origins = [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]
    #     return origins

    # @field_validator('allowed_origins', mode='before')
    # @classmethod
    # def parse_cors_origins(cls, v):
    #     """Parse CORS origins from string or list."""
    #     if isinstance(v, str):
    #         # Split comma-separated string
    #         return [origin.strip() for origin in v.split(',') if origin.strip()]
    #     return v
    
    # ==================== Database Configuration ====================
    database_url: str = ""
    
    # ==================== GEmini/Anthropic API Configuration ====================
    #anthropic_api_key: str = ""
    #anthropic_model: str = "claude-sonnet-4-20250514"
    ai_provider: str = "gemini"  # or "anthropic" if you switch back
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"  # Free tier model
    max_tokens: int = 2048  # Gemini calls this "max_output_tokens"
    temperature: float = 0.7
    
    # ==================== AI Agent Configuration ====================
    ai_agent_name: str = "Howard's Portfolio Assistant"
    ai_agent_role: str = "AI assistant helping recruiters learn about Howard Ye"
    
    # ==================== Security ====================
    secret_key: str = "your-secret-key-change-this-in-production"
    
    # ==================== Rate Limiting ====================
    rate_limit_per_minute: int = 10
    
    # class Config:
    #     env_file = ".env"
    #     case_sensitive = False


# ==================== Global Settings Instance ====================
settings = Settings()
