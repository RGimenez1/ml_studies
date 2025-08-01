"""
Dependency injection container.
"""
import logging
from .config import AppConfig
from .use_cases import ModelInitializationUseCase, PredictionUseCase, HealthCheckUseCase
from ..infrastructure.kaggle_dataset_repository import KaggleDatasetRepository
from ..infrastructure.file_model_repository import FileModelRepository
from ..infrastructure.sklearn_ml_trainer import SklearnMLTrainer
from ..api.controllers import MLController


class Container:
    """Dependency injection container."""

    def __init__(self, config: AppConfig):
        self.config = config
        self._setup_logging()
        self._instances = {}

    def _setup_logging(self):
        """Setup application logging."""
        logging.basicConfig(
            level=getattr(logging, self.config.logging.level),
            format=self.config.logging.format
        )

    def get_dataset_repository(self) -> KaggleDatasetRepository:
        """Get dataset repository instance."""
        if "dataset_repo" not in self._instances:
            self._instances["dataset_repo"] = KaggleDatasetRepository(
                dataset_id=self.config.kaggle.dataset_id,
                csv_filename=self.config.kaggle.csv_filename,
                dev_mode=self.config.ml.dev_mode,
                sample_size=self.config.ml.sample_size
            )
        return self._instances["dataset_repo"]

    def get_model_repository(self) -> FileModelRepository:
        """Get model repository instance."""
        if "model_repo" not in self._instances:
            self._instances["model_repo"] = FileModelRepository(
                models_dir=self.config.database.models_dir
            )
        return self._instances["model_repo"]

    def get_ml_trainer(self) -> SklearnMLTrainer:
        """Get ML trainer instance."""
        if "ml_trainer" not in self._instances:
            self._instances["ml_trainer"] = SklearnMLTrainer(
                use_fast_model=self.config.ml.use_fast_model,
                n_jobs=self.config.ml.n_jobs
            )
        return self._instances["ml_trainer"]

    def get_model_init_use_case(self) -> ModelInitializationUseCase:
        """Get model initialization use case."""
        if "model_init_use_case" not in self._instances:
            self._instances["model_init_use_case"] = ModelInitializationUseCase(
                dataset_repo=self.get_dataset_repository(),
                model_repo=self.get_model_repository(),
                ml_trainer=self.get_ml_trainer()
            )
        return self._instances["model_init_use_case"]

    def get_prediction_use_case(self) -> PredictionUseCase:
        """Get prediction use case."""
        if "prediction_use_case" not in self._instances:
            self._instances["prediction_use_case"] = PredictionUseCase(
                ml_trainer=self.get_ml_trainer(),
                model_init_use_case=self.get_model_init_use_case()
            )
        return self._instances["prediction_use_case"]

    def get_health_check_use_case(self) -> HealthCheckUseCase:
        """Get health check use case."""
        if "health_check_use_case" not in self._instances:
            self._instances["health_check_use_case"] = HealthCheckUseCase(
                model_init_use_case=self.get_model_init_use_case()
            )
        return self._instances["health_check_use_case"]

    def get_ml_controller(self) -> MLController:
        """Get ML controller instance."""
        if "ml_controller" not in self._instances:
            self._instances["ml_controller"] = MLController(
                model_init_use_case=self.get_model_init_use_case(),
                prediction_use_case=self.get_prediction_use_case(),
                health_check_use_case=self.get_health_check_use_case()
            )
        return self._instances["ml_controller"]