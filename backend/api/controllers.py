"""
FastAPI controllers for handling HTTP requests.
"""
from fastapi import HTTPException
import logging

from ..core.use_cases import ModelInitializationUseCase, PredictionUseCase, HealthCheckUseCase
from ..domain.entities import PredictionRequest


logger = logging.getLogger(__name__)


class MLController:
    """Controller for ML-related endpoints."""

    def __init__(
        self,
        model_init_use_case: ModelInitializationUseCase,
        prediction_use_case: PredictionUseCase,
        health_check_use_case: HealthCheckUseCase,
    ):
        self.model_init_use_case = model_init_use_case
        self.prediction_use_case = prediction_use_case
        self.health_check_use_case = health_check_use_case

    async def initialize(self):
        """Initialize the ML models."""
        try:
            result = self.model_init_use_case.execute()
            logger.info("Models initialized successfully")
            return result
        except Exception as e:
            logger.error(f"Model initialization failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def predict(self, input_data: dict):
        """Make predictions based on input parameters."""
        try:
            if not self.model_init_use_case.is_initialized:
                raise HTTPException(status_code=400, detail="Models not trained yet")

            # Convert input to domain entity
            request = PredictionRequest.from_dict(input_data)
            
            # Execute prediction
            result = self.prediction_use_case.execute(request)
            
            return {
                "status": "success",
                "predictions": result.predictions.to_dict()
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    async def health(self):
        """Health check endpoint."""
        try:
            return self.health_check_use_case.execute()
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))