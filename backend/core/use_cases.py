"""
Use cases implementing business logic.
"""
from typing import Dict, Optional
from datetime import datetime
import logging

from ..domain.entities import (
    PredictionRequest, 
    PredictionResult, 
    TirePredictions, 
    FeatureRange, 
    ModelMetadata
)
from ..domain.repositories import DatasetRepository, ModelRepository, MLModelTrainer


logger = logging.getLogger(__name__)


class ModelInitializationUseCase:
    """Use case for initializing ML models."""

    def __init__(
        self,
        dataset_repo: DatasetRepository,
        model_repo: ModelRepository,
        ml_trainer: MLModelTrainer,
    ):
        self.dataset_repo = dataset_repo
        self.model_repo = model_repo
        self.ml_trainer = ml_trainer
        self._models = None
        self._feature_ranges = None
        self._metadata = None

    def execute(self) -> Dict:
        """Initialize models by loading existing ones or training new ones."""
        try:
            # Try to load existing models first
            if self.model_repo.models_exist():
                logger.info("Loading existing models...")
                self._models = self.model_repo.load_models()
                self._feature_ranges = self.model_repo.load_feature_ranges()
                self._metadata = self.model_repo.load_metadata()
                
                if self._models and self._feature_ranges:
                    logger.info(f"Models loaded successfully! Trained at: {self._metadata.trained_at}")
                    return self._create_success_response()

            # Train new models if loading failed or models don't exist
            logger.info("Training new models...")
            return self._train_new_models()

        except Exception as e:
            logger.error(f"Model initialization failed: {e}")
            raise

    def _train_new_models(self) -> Dict:
        """Train new models from scratch."""
        start_time = datetime.now()
        
        # Load training data
        data = self.dataset_repo.load_training_data()
        logger.info(f"Loaded dataset with {len(data)} samples")

        # Define target variables
        variables = [
            "Speed", "Throttle", "Brake", "Surface_Roughness",
            "front_surface_temp", "rear_surface_temp", "force_on_tire",
            "Tire_wear", "Tire degreadation", "cumilative_Tire_Wear"
        ]

        # Calculate feature ranges
        self._feature_ranges = self.dataset_repo.get_feature_ranges(data)

        # Train models
        self._models = self.ml_trainer.train_models(data, variables)

        # Create metadata
        end_time = datetime.now()
        training_duration = (end_time - start_time).total_seconds()
        self._metadata = ModelMetadata(
            trained_at=end_time,
            model_count=len(self._models),
            version="1.0",
            training_duration=training_duration
        )

        # Save models for future use
        self.model_repo.save_models(self._models, self._feature_ranges, self._metadata)
        logger.info(f"Models trained and saved in {training_duration:.1f}s")

        return self._create_success_response()

    def _create_success_response(self) -> Dict:
        """Create a successful initialization response."""
        feature_ranges_dict = {
            name: range_obj.to_dict() 
            for name, range_obj in self._feature_ranges.items()
        }
        
        return {
            "status": "success",
            "feature_ranges": feature_ranges_dict,
            "variables": list(self._feature_ranges.keys()),
            "metadata": self._metadata.to_dict() if self._metadata else None
        }

    @property
    def is_initialized(self) -> bool:
        """Check if models are initialized."""
        return self._models is not None and self._feature_ranges is not None

    @property
    def models(self) -> Optional[Dict]:
        """Get the loaded models."""
        return self._models

    @property
    def feature_ranges(self) -> Optional[Dict[str, FeatureRange]]:
        """Get the feature ranges."""
        return self._feature_ranges


class PredictionUseCase:
    """Use case for making tire wear predictions."""

    def __init__(
        self,
        ml_trainer: MLModelTrainer,
        model_init_use_case: ModelInitializationUseCase,
    ):
        self.ml_trainer = ml_trainer
        self.model_init_use_case = model_init_use_case

    def execute(self, request: PredictionRequest) -> PredictionResult:
        """Execute prediction based on input parameters."""
        if not self.model_init_use_case.is_initialized:
            raise ValueError("Models not initialized. Call initialization first.")

        try:
            # Make predictions
            input_dict = request.parameters.to_dict()
            raw_predictions = self.ml_trainer.predict(
                self.model_init_use_case.models, 
                input_dict
            )

            # Convert to domain entities
            predictions = TirePredictions(
                tire_wear=raw_predictions.get("Tire_wear", 0.0),
                tire_degradation=raw_predictions.get("Tire degreadation", 0.0),
                cumulative_tire_wear=raw_predictions.get("cumilative_Tire_Wear", 0.0),
            )

            return PredictionResult(
                predictions=predictions,
                input_parameters=request.parameters,
            )

        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise


class HealthCheckUseCase:
    """Use case for health check operations."""

    def __init__(self, model_init_use_case: ModelInitializationUseCase):
        self.model_init_use_case = model_init_use_case

    def execute(self) -> Dict[str, any]:
        """Execute health check."""
        return {
            "status": "healthy",
            "trained": self.model_init_use_case.is_initialized,
            "timestamp": datetime.now().isoformat(),
        }