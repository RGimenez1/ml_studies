"""
Kaggle dataset repository implementation.
"""
import pandas as pd
import pathlib
import kagglehub
import logging
from typing import Dict

from ..domain.repositories import DatasetRepository
from ..domain.entities import FeatureRange


logger = logging.getLogger(__name__)


class KaggleDatasetRepository(DatasetRepository):
    """Repository for loading data from Kaggle datasets."""

    def __init__(self, dataset_id: str, csv_filename: str, dev_mode: bool = True, sample_size: float = 0.05):
        self.dataset_id = dataset_id
        self.csv_filename = csv_filename
        self.dev_mode = dev_mode
        self.sample_size = sample_size

    def load_training_data(self) -> pd.DataFrame:
        """Load training data from Kaggle dataset."""
        logger.info(f"Loading dataset: {self.dataset_id}")
        
        path = kagglehub.dataset_download(self.dataset_id)
        data_dir = pathlib.Path(path)
        data = pd.read_csv(data_dir / self.csv_filename)
        
        # Sample data for faster development if in dev_mode
        if self.dev_mode and len(data) > 1000:
            sample_n = int(len(data) * self.sample_size)
            data = data.sample(n=sample_n, random_state=42)
            logger.info(f"Development mode: Using {sample_n} samples ({self.sample_size*100:.1f}% of dataset)")
        
        logger.info(f"Loaded {len(data)} samples")
        return data

    def get_feature_ranges(self, data: pd.DataFrame) -> Dict[str, FeatureRange]:
        """Calculate feature ranges from the dataset."""
        variables = [
            "Speed", "Throttle", "Brake", "Surface_Roughness",
            "front_surface_temp", "rear_surface_temp", "force_on_tire",
            "Tire_wear", "Tire degreadation", "cumilative_Tire_Wear"
        ]
        
        feature_ranges = {}
        for var in variables:
            if var in data.columns:
                feature_ranges[var] = FeatureRange(
                    min_value=float(data[var].min()),
                    max_value=float(data[var].max()),
                    mean_value=float(data[var].mean()),
                    median_value=float(data[var].median()),
                )
        
        return feature_ranges