"""
Repository interfaces defining contracts for data access.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, List
import pandas as pd
from .entities import ModelMetadata, FeatureRange


class DatasetRepository(ABC):
    """Abstract repository for dataset operations."""

    @abstractmethod
    def load_training_data(self) -> pd.DataFrame:
        """Load the training dataset."""
        pass

    @abstractmethod
    def get_feature_ranges(self, data: pd.DataFrame) -> Dict[str, FeatureRange]:
        """Calculate and return feature ranges from dataset."""
        pass


class ModelRepository(ABC):
    """Abstract repository for model persistence operations."""

    @abstractmethod
    def save_models(self, models: Dict, feature_ranges: Dict[str, FeatureRange], metadata: ModelMetadata) -> bool:
        """Save trained models, feature ranges, and metadata."""
        pass

    @abstractmethod
    def load_models(self) -> Optional[Dict]:
        """Load trained models if they exist."""
        pass

    @abstractmethod
    def load_feature_ranges(self) -> Optional[Dict[str, FeatureRange]]:
        """Load feature ranges if they exist."""
        pass

    @abstractmethod
    def load_metadata(self) -> Optional[ModelMetadata]:
        """Load model metadata if it exists."""
        pass

    @abstractmethod
    def models_exist(self) -> bool:
        """Check if saved models exist."""
        pass


class MLModelTrainer(ABC):
    """Abstract interface for ML model training."""

    @abstractmethod
    def train_models(self, data: pd.DataFrame, variables: List[str]) -> Dict:
        """Train ML models for all target variables."""
        pass

    @abstractmethod
    def predict(self, models: Dict, input_data: Dict[str, float]) -> Dict[str, float]:
        """Make predictions using trained models."""
        pass