from starlette.config import Config
from starlette.datastructures import Secret, CommaSeparatedStrings, URL
from typing import Optional, Dict, Any
import os
import json
from carpenter_py.env import project_root

class CarpenterConfig:
    """
    Configuration management for Carpenter applications.
    Loads configuration from environment variables and/or .env files.
    """

    def __init__(self, env_file: Optional[str] = None) -> None:
        """
        Initialize configuration with optional env file.

        Args:
            env_file: Path to .env file, defaults to None
        """
        self.file = os.path.join(project_root, '.env')
        self.config = Config(env_file=env_file)
        self.config.env_prefix = "CARPENTER_"

    # Basic Settings
    @property
    def DEBUG(self) -> bool:
        """Flag for debug mode"""
        return self.config("DEBUG", cast=bool, default=False)

    @property
    def ENVIRONMENT(self) -> str:
        """Current environment (development, testing, production)"""
        return self.config("ENVIRONMENT", default="development")

    @property
    def APP_NAME(self) -> str:
        """Application name"""
        return self.config("APP_NAME", default="Carpenter App")

    @property
    def VERSION(self) -> str:
        """Application version"""
        return self.config("VERSION", default="0.1.0")

    # Security Settings
    @property
    def SECRET_KEY(self) -> Secret:
        """Secret key for cryptographic signing"""
        return self.config("SECRET_KEY", cast=Secret)

    @property
    def ALLOWED_HOSTS(self) -> CommaSeparatedStrings:
        """Allowed hostnames"""
        return self.config(
            "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="localhost,127.0.0.1"
        )

    @property
    def CORS_ORIGINS(self) -> CommaSeparatedStrings:
        """Allowed CORS origins"""
        return self.config(
            "CORS_ORIGINS", cast=CommaSeparatedStrings, default="http://localhost:3000"
        )

    @property
    def AUTH_REQUIRED(self) -> bool:
        """Whether authentication is required for all endpoints"""
        return self.config("AUTH_REQUIRED", cast=bool, default=True)

    @property
    def JWT_EXPIRATION_DELTA(self) -> int:
        """JWT token expiration in seconds"""
        return self.config("JWT_EXPIRATION_DELTA", cast=int, default=86400)  # 24 hours

    # Database Settings
    @property
    def DATABASE_URL(self) -> URL:
        """Database connection URL"""
        return self.config("DATABASE_URL", cast=URL)

    @property
    def DATABASE_POOL_SIZE(self) -> int:
        """Database connection pool size"""
        return self.config("DATABASE_POOL_SIZE", cast=int, default=5)

    @property
    def DATABASE_MAX_OVERFLOW(self) -> int:
        """Maximum number of connections that can be created beyond pool size"""
        return self.config("DATABASE_MAX_OVERFLOW", cast=int, default=10)

    @property
    def DATABASE_ECHO(self) -> bool:
        """Whether to log SQL queries"""
        return self.config("DATABASE_ECHO", cast=bool, default=False)

    @property
    def MIGRATIONS_DIR(self) -> str:
        """Database migrations directory"""
        return self.config("MIGRATIONS_DIR", default="migrations")

    # Cache Settings
    @property
    def REDIS_URL(self) -> Optional[URL]:
        """Redis connection URL"""
        return self.config("REDIS_URL", cast=URL, default=None)

    @property
    def CACHE_TTL(self) -> int:
        """Default cache TTL in seconds"""
        return self.config("CACHE_TTL", cast=int, default=300)  # 5 minutes

    # File Storage Settings
    @property
    def STORAGE_TYPE(self) -> str:
        """Storage type (local, s3, etc.)"""
        return self.config("STORAGE_TYPE", default="local")

    @property
    def STORAGE_ROOT(self) -> str:
        """Local storage root directory"""
        return self.config("STORAGE_ROOT", default="media")

    @property
    def S3_BUCKET_NAME(self) -> Optional[str]:
        """AWS S3 bucket name"""
        return self.config("S3_BUCKET_NAME", default=None)

    @property
    def S3_REGION(self) -> Optional[str]:
        """AWS S3 region"""
        return self.config("S3_REGION", default=None)

    # Email Settings
    @property
    def SMTP_HOST(self) -> Optional[str]:
        """SMTP server host"""
        return self.config("SMTP_HOST", default=None)

    @property
    def SMTP_PORT(self) -> int:
        """SMTP server port"""
        return self.config("SMTP_PORT", cast=int, default=587)

    @property
    def SMTP_USER(self) -> Optional[str]:
        """SMTP username"""
        return self.config("SMTP_USER", default=None)

    @property
    def SMTP_PASSWORD(self) -> Optional[Secret]:
        """SMTP password"""
        return self.config("SMTP_PASSWORD", cast=Secret, default=None)

    @property
    def EMAIL_FROM(self) -> str:
        """Default sender email address"""
        return self.config("EMAIL_FROM", default="noreply@example.com")

    # Logging Settings
    @property
    def LOG_LEVEL(self) -> str:
        """Logging level"""
        return self.config("LOG_LEVEL", default="critical")

    @property
    def LOG_FORMAT(self) -> str:
        """Logging format"""
        return self.config("LOG_FORMAT", default="%(levelname)s:%(name)s:%(message)s")

    @property
    def LOG_FILE(self) -> Optional[str]:
        """Log file path"""
        return self.config("LOG_FILE", default=None)

    # API Settings
    @property
    def API_VERSION(self) -> str:
        """API version"""
        return self.config("API_VERSION", default="v1")

    @property
    def RATE_LIMIT_PER_MINUTE(self) -> int:
        """API rate limit per minute"""
        return self.config("RATE_LIMIT_PER_MINUTE", cast=int, default=60)

    @property
    def VITE_PORT(self) -> int:
        """Vite port"""
        return self.config("VITE_PORT", cast=int, default=4000)

    # Third-party Integration Settings
    @property
    def SENTRY_DSN(self) -> Optional[str]:
        """Sentry DSN for error tracking"""
        return self.config("SENTRY_DSN", default=None)

    @property
    def STRIPE_API_KEY(self) -> Optional[Secret]:
        """Stripe API key for payments"""
        return self.config("STRIPE_API_KEY", cast=Secret, default=None)

    @property
    def GITHUB_CLIENT_ID(self) -> Optional[str]:
        """GitHub OAuth client ID"""
        return self.config("GITHUB_CLIENT_ID", default=None)

    @property
    def GITHUB_CLIENT_SECRET(self) -> Optional[Secret]:
        """GitHub OAuth client secret"""
        return self.config("GITHUB_CLIENT_SECRET", cast=Secret, default=None)

    # Utility Methods
    def get(self, key: str, default: Any = None, cast: Any = None) -> Any:
        """
        Get a configuration value with optional default and casting.

        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            cast: Function to cast the value

        Returns:
            The configuration value
        """
        return self.config(key, default=default, cast=cast)

    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values as a dictionary.
        Only includes non-secret values.

        Returns:
            Dictionary of configuration values
        """
        result = {}
        for key in dir(self):
            if key.isupper() and not key.startswith("_"):
                value = getattr(self, key)
                # Skip Secret values
                if not isinstance(value, Secret):
                    result[key] = value
        return result

    def from_json(self, json_file: str) -> None:
        """
        Load configuration from JSON file.

        Args:
            json_file: Path to JSON configuration file
        """
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"Configuration file {json_file} not found")

        with open(json_file, "r") as f:
            config_data = json.load(f)

        for key, value in config_data.items():
            env_key = f"CARPENTER_{key}"
            if env_key not in os.environ:
                os.environ[env_key] = str(value)

    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT.lower() == "development"

    def is_testing(self) -> bool:
        """Check if running in testing environment"""
        return self.ENVIRONMENT.lower() == "testing"

    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT.lower() == "production"
