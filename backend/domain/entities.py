"""
Domain entities representing core business concepts.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class TireParameters:
    """Represents tire-related input parameters."""
    speed: float
    throttle: float
    brake: float
    surface_roughness: float
    front_surface_temp: float
    rear_surface_temp: float
    force_on_tire: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "Speed": self.speed,
            "Throttle": self.throttle,
            "Brake": self.brake,
            "Surface_Roughness": self.surface_roughness,
            "front_surface_temp": self.front_surface_temp,
            "rear_surface_temp": self.rear_surface_temp,
            "force_on_tire": self.force_on_tire,
        }


@dataclass
class TirePredictions:
    """Represents tire wear prediction results."""
    tire_wear: float
    tire_degradation: float
    cumulative_tire_wear: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "Tire_wear": self.tire_wear,
            "Tire degreadation": self.tire_degradation,
            "cumilative_Tire_Wear": self.cumulative_tire_wear,
        }


@dataclass
class FeatureRange:
    """Represents the statistical range of a feature."""
    min_value: float
    max_value: float
    mean_value: float
    median_value: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "min": self.min_value,
            "max": self.max_value,
            "mean": self.mean_value,
            "median": self.median_value,
        }


@dataclass
class ModelMetadata:
    """Represents metadata about trained models."""
    trained_at: datetime
    model_count: int
    version: str
    training_duration: Optional[float] = None

    def to_dict(self) -> Dict:
        return {
            "trained_at": self.trained_at.isoformat(),
            "model_count": self.model_count,
            "version": self.version,
            "training_duration": self.training_duration,
        }


@dataclass
class PredictionRequest:
    """Represents a prediction request."""
    parameters: TireParameters

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "PredictionRequest":
        return cls(
            parameters=TireParameters(
                speed=data.get("Speed", 0.0),
                throttle=data.get("Throttle", 0.0),
                brake=data.get("Brake", 0.0),
                surface_roughness=data.get("Surface_Roughness", 0.0),
                front_surface_temp=data.get("front_surface_temp", 0.0),
                rear_surface_temp=data.get("rear_surface_temp", 0.0),
                force_on_tire=data.get("force_on_tire", 0.0),
            )
        )


@dataclass
class PredictionResult:
    """Represents the complete prediction result."""
    predictions: TirePredictions
    input_parameters: TireParameters
    model_metadata: Optional[ModelMetadata] = None

    def to_dict(self) -> Dict:
        result = {
            "predictions": self.predictions.to_dict(),
            "input_parameters": self.input_parameters.to_dict(),
        }
        if self.model_metadata:
            result["metadata"] = self.model_metadata.to_dict()
        return result