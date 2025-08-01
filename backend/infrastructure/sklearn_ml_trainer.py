"""
Scikit-learn ML trainer implementation.
"""
import pandas as pd
import logging
from typing import Dict, List
from datetime import datetime
from joblib import Parallel, delayed
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from ..domain.repositories import MLModelTrainer


logger = logging.getLogger(__name__)


class SklearnMLTrainer(MLModelTrainer):
    """ML trainer using scikit-learn models."""

    def __init__(self, use_fast_model: bool = True, n_jobs: int = -1):
        self.use_fast_model = use_fast_model
        self.n_jobs = n_jobs

    def train_models(self, data: pd.DataFrame, variables: List[str]) -> Dict:
        """Train ML models for all target variables using parallel processing."""
        start_time = datetime.now()
        logger.info(f"Training models... Started at {start_time.strftime('%H:%M:%S')}")
        
        # Train models in parallel
        model_results = Parallel(n_jobs=self.n_jobs)(
            delayed(self._train_single_model)(data, variables, target_var) 
            for target_var in variables
        )
        
        # Store results
        models = {}
        for target_var, model_info in model_results:
            models[target_var] = model_info
            
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        logger.info(f"All models trained in {total_duration:.1f}s (finished at {end_time.strftime('%H:%M:%S')})")

        return models

    def _train_single_model(self, data: pd.DataFrame, variables: List[str], target_var: str):
        """Train a single model for a target variable."""
        model_start = datetime.now()
        logger.info(f"[{model_start.strftime('%H:%M:%S')}] Training model for {target_var}...")
        
        feature_vars = [var for var in variables if var != target_var]

        X = data[feature_vars].fillna(0)
        y = data[target_var].fillna(0)

        if self.use_fast_model:
            model = LinearRegression()
        else:
            model = RandomForestRegressor(n_estimators=15, random_state=42)
        
        model.fit(X, y)
        
        model_end = datetime.now()
        duration = (model_end - model_start).total_seconds()
        logger.info(f"[{model_end.strftime('%H:%M:%S')}] Completed {target_var} in {duration:.1f}s")
        
        return target_var, {"model": model, "features": feature_vars}

    def predict(self, models: Dict, input_data: Dict[str, float]) -> Dict[str, float]:
        """Make predictions using trained models."""
        predictions = {}

        for target_var, model_info in models.items():
            model = model_info["model"]
            features = model_info["features"]

            # Prepare feature vector with default values for missing features
            feature_vector = [
                input_data.get(f, 0.0) for f in features
            ]

            # Create DataFrame with proper feature names to match training
            feature_df = pd.DataFrame([feature_vector], columns=features)
            
            # Make prediction
            prediction = model.predict(feature_df)[0]
            predictions[target_var] = float(prediction)

        return predictions