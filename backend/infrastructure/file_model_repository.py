"""
File-based model repository implementation.
"""
import os
import json
import pickle
import logging
from typing import Dict, Optional
from datetime import datetime

from ..domain.repositories import ModelRepository
from ..domain.entities import ModelMetadata, FeatureRange


logger = logging.getLogger(__name__)


class FileModelRepository(ModelRepository):
    """Repository for persisting models to local files."""

    def __init__(self, models_dir: str = "saved_models"):
        self.models_dir = models_dir
        self.models_file = os.path.join(models_dir, "ml_models.pkl")
        self.ranges_file = os.path.join(models_dir, "feature_ranges.pkl")
        self.metadata_file = os.path.join(models_dir, "metadata.json")
        
        # Create models directory if it doesn't exist
        os.makedirs(models_dir, exist_ok=True)

    def save_models(self, models: Dict, feature_ranges: Dict[str, FeatureRange], metadata: ModelMetadata) -> bool:
        """Save trained models, feature ranges, and metadata to files."""
        try:
            logger.info("Saving models to disk...")

            # Save models
            with open(self.models_file, "wb") as f:
                pickle.dump(models, f)

            # Save feature ranges (convert to dict for serialization)
            ranges_dict = {name: range_obj.to_dict() for name, range_obj in feature_ranges.items()}
            with open(self.ranges_file, "wb") as f:
                pickle.dump(ranges_dict, f)

            # Save metadata
            with open(self.metadata_file, "w") as f:
                json.dump(metadata.to_dict(), f, indent=2)

            logger.info(f"Models saved successfully at {datetime.now()}")
            return True

        except Exception as e:
            logger.error(f"Failed to save models: {e}")
            return False

    def load_models(self) -> Optional[Dict]:
        """Load trained models from file."""
        try:
            with open(self.models_file, "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, pickle.PickleError) as e:
            logger.warning(f"Could not load models: {e}")
            return None

    def load_feature_ranges(self) -> Optional[Dict[str, FeatureRange]]:
        """Load feature ranges from file."""
        try:
            with open(self.ranges_file, "rb") as f:
                ranges_dict = pickle.load(f)
                
            # Convert back to FeatureRange objects
            feature_ranges = {}
            for name, range_data in ranges_dict.items():
                feature_ranges[name] = FeatureRange(
                    min_value=range_data["min"],
                    max_value=range_data["max"],
                    mean_value=range_data["mean"],
                    median_value=range_data["median"],
                )
            
            return feature_ranges
        except (FileNotFoundError, pickle.PickleError) as e:
            logger.warning(f"Could not load feature ranges: {e}")
            return None

    def load_metadata(self) -> Optional[ModelMetadata]:
        """Load model metadata from file."""
        try:
            with open(self.metadata_file, "r") as f:
                metadata_dict = json.load(f)
            
            return ModelMetadata(
                trained_at=datetime.fromisoformat(metadata_dict["trained_at"]),
                model_count=metadata_dict["model_count"],
                version=metadata_dict["version"],
                training_duration=metadata_dict.get("training_duration"),
            )
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.warning(f"Could not load metadata: {e}")
            return None

    def models_exist(self) -> bool:
        """Check if all required model files exist."""
        return (
            os.path.exists(self.models_file) and
            os.path.exists(self.ranges_file) and
            os.path.exists(self.metadata_file)
        )