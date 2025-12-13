from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    app_name: str = "BeyondFit"
    app_env: str = "development"
    debug: bool = True
    api_version: str = "v1"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    allowed_origins: str = "http://localhost:3000,http://localhost:19006"
    
    # Database
    database_url: str
    
    # Auth
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""
    supabase_service_key: str = ""
    
    # Storage
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    s3_bucket_name: str = "beyondfit-photos"
    s3_endpoint_url: str = ""
    
    # Privacy
    delete_photos_after_processing: bool = True
    photo_retention_hours: int = 0
    
    # Email
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    from_email: str = "noreply@beyondfit.com"
    
    # Affiliate
    affiliate_click_tracking: bool = True
    affiliate_conversion_webhook: str = ""
    
    # Rate limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    
    # Features
    enable_admin_api: bool = True
    enable_analytics: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
