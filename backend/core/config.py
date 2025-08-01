"""
Application configuration.
"""

from dataclasses import dataclass
from typing import Dict, Any
import os


@dataclass
class DatabaseConfig:
    """Configuration for database-related settings."""

    models_dir: str = "saved_models"


@dataclass
class KaggleConfig:
    """Configuration for Kaggle dataset."""

    dataset_id: str = "samwelnjehia/simple-tire-wear-and-degradation-simulated-dataset"
    csv_filename: str = "simulated_dataset.csv"


@dataclass
class MLConfig:
    """Configuration for ML training."""

    dev_mode: bool = True
    sample_size: float = 0.05
    use_fast_model: bool = False
    n_jobs: int = -1


@dataclass
class APIConfig:
    """Configuration for API server."""

    host: str = "0.0.0.0"
    port: int = 5000
    title: str = "ML Tire Wear Predictor API"
    version: str = "1.0.0"
    cors_origins: list = None

    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["*"]


@dataclass
class LoggingConfig:
    """Configuration for logging."""

    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@dataclass
class AppConfig:
    """Main application configuration."""

    database: DatabaseConfig
    kaggle: KaggleConfig
    ml: MLConfig
    api: APIConfig
    logging: LoggingConfig

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Create configuration from environment variables."""
        return cls(
            database=DatabaseConfig(models_dir=os.getenv("MODELS_DIR", "saved_models")),
            kaggle=KaggleConfig(
                dataset_id=os.getenv(
                    "KAGGLE_DATASET_ID",
                    "samwelnjehia/simple-tire-wear-and-degradation-simulated-dataset",
                ),
                csv_filename=os.getenv("CSV_FILENAME", "simulated_dataset.csv"),
            ),
            ml=MLConfig(
                dev_mode=os.getenv("DEV_MODE", "true").lower() == "true",
                sample_size=float(os.getenv("SAMPLE_SIZE", "0.05")),
                use_fast_model=os.getenv("USE_FAST_MODEL", "False").lower() == "true",
                n_jobs=int(os.getenv("N_JOBS", "-1")),
            ),
            api=APIConfig(
                host=os.getenv("API_HOST", "0.0.0.0"),
                port=int(os.getenv("API_PORT", "5000")),
                title=os.getenv("API_TITLE", "ML Tire Wear Predictor API"),
                version=os.getenv("API_VERSION", "1.0.0"),
                cors_origins=os.getenv("CORS_ORIGINS", "*").split(","),
            ),
            logging=LoggingConfig(
                level=os.getenv("LOG_LEVEL", "INFO"),
                format=os.getenv(
                    "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                ),
            ),
        )
