from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from joblib import Parallel, delayed
import pathlib
import kagglehub
import json
import pickle
import os
from datetime import datetime

app = FastAPI(title="ML Tire Wear Predictor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MLPredictor:
    def __init__(self, dev_mode=True, sample_size=0.2, use_fast_model=True):
        self.models = {}
        self.feature_ranges = {}
        self.is_trained = False
        self.models_dir = "saved_models"
        self.models_file = os.path.join(self.models_dir, "ml_models.pkl")
        self.ranges_file = os.path.join(self.models_dir, "feature_ranges.pkl")
        self.metadata_file = os.path.join(self.models_dir, "metadata.json")
        self.dev_mode = dev_mode
        self.sample_size = sample_size
        self.use_fast_model = use_fast_model

        # Create models directory if it doesn't exist
        os.makedirs(self.models_dir, exist_ok=True)

    def save_models(self):
        """Save trained models and metadata to disk"""
        print("Saving models to disk...")

        # Save models
        with open(self.models_file, "wb") as f:
            pickle.dump(self.models, f)

        # Save feature ranges
        with open(self.ranges_file, "wb") as f:
            pickle.dump(self.feature_ranges, f)

        # Save metadata
        metadata = {
            "trained_at": datetime.now().isoformat(),
            "model_count": len(self.models),
            "version": "1.0",
        }
        with open(self.metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"Models saved successfully at {datetime.now()}")

    def load_models(self):
        """Load trained models from disk"""
        try:
            print("Loading models from disk...")

            # Load models
            with open(self.models_file, "rb") as f:
                self.models = pickle.load(f)

            # Load feature ranges
            with open(self.ranges_file, "rb") as f:
                self.feature_ranges = pickle.load(f)

            # Load metadata
            with open(self.metadata_file, "r") as f:
                metadata = json.load(f)

            self.is_trained = True
            print(f"Models loaded successfully! Trained at: {metadata['trained_at']}")
            return True

        except (FileNotFoundError, pickle.PickleError, json.JSONDecodeError) as e:
            print(f"Could not load saved models: {e}")
            return False

    def models_exist(self):
        """Check if saved models exist"""
        return (
            os.path.exists(self.models_file)
            and os.path.exists(self.ranges_file)
            and os.path.exists(self.metadata_file)
        )

    def load_and_train(self):
        """Load data and train models (with caching)"""
        # Try to load existing models first
        if self.models_exist() and self.load_models():
            print("Using cached models - no retraining needed!")
            return

        print("No cached models found. Training new models...")
        print("Loading dataset...")
        path = kagglehub.dataset_download(
            "samwelnjehia/simple-tire-wear-and-degradation-simulated-dataset"
        )
        DATA_DIR = pathlib.Path(path)
        data = pd.read_csv(DATA_DIR / "simulated_dataset.csv")
        
        # Sample data for faster development if in dev_mode
        if self.dev_mode and len(data) > 1000:
            sample_n = int(len(data) * self.sample_size)
            data = data.sample(n=sample_n, random_state=42)
            print(f"Development mode: Using {sample_n} samples ({self.sample_size*100:.1f}% of dataset)")

        # Define all variables
        all_variables = [
            "Speed",
            "Throttle",
            "Brake",
            "Surface_Roughness",
            "front_surface_temp",
            "rear_surface_temp",
            "force_on_tire",
            "Tire_wear",
            "Tire degreadation",
            "cumilative_Tire_Wear",
        ]

        # Store feature ranges for sliders
        for var in all_variables:
            self.feature_ranges[var] = {
                "min": float(data[var].min()),
                "max": float(data[var].max()),
                "mean": float(data[var].mean()),
                "median": float(data[var].median()),
            }

        # Train models in parallel
        start_time = datetime.now()
        print(f"Training models... Started at {start_time.strftime('%H:%M:%S')}")
        
        def train_single_model(target_var):
            model_start = datetime.now()
            print(f"[{model_start.strftime('%H:%M:%S')}] Training model for {target_var}...")
            feature_vars = [var for var in all_variables if var != target_var]

            X = data[feature_vars].fillna(0)
            y = data[target_var].fillna(0)

            if self.use_fast_model:
                model = LinearRegression()
            else:
                model = RandomForestRegressor(n_estimators=15, random_state=42)
            model.fit(X, y)
            
            model_end = datetime.now()
            duration = (model_end - model_start).total_seconds()
            print(f"[{model_end.strftime('%H:%M:%S')}] Completed {target_var} in {duration:.1f}s")
            return target_var, {"model": model, "features": feature_vars}

        # Train models in parallel
        model_results = Parallel(n_jobs=-1)(
            delayed(train_single_model)(target_var) for target_var in all_variables
        )
        
        # Store results
        for target_var, model_info in model_results:
            self.models[target_var] = model_info
            
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        print(f"All models trained in {total_duration:.1f}s (finished at {end_time.strftime('%H:%M:%S')})")

        self.is_trained = True
        print("Models trained successfully!")

        # Save models for future use
        self.save_models()

    def predict_all(self, input_values):
        """Predict all variables based on input values"""
        if not self.is_trained:
            return None

        predictions = {}

        for target_var, model_info in self.models.items():
            model = model_info["model"]
            features = model_info["features"]

            # Prepare feature vector
            feature_vector = [
                input_values.get(f, self.feature_ranges[f]["median"]) for f in features
            ]

            # Make prediction
            prediction = model.predict([feature_vector])[0]
            predictions[target_var] = float(prediction)

        return predictions


# Global predictor instance (use smaller sample and fast algorithm for development)
predictor = MLPredictor(dev_mode=True, sample_size=0.05, use_fast_model=True)


@app.get("/api/initialize")
def initialize():
    """Initialize the ML models"""
    try:
        if not predictor.is_trained:
            predictor.load_and_train()

        return {
            "status": "success",
            "feature_ranges": predictor.feature_ranges,
            "variables": list(predictor.feature_ranges.keys()),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict")
def predict(input_data: dict):
    """Make predictions based on input parameters"""
    try:
        if not predictor.is_trained:
            raise HTTPException(status_code=400, detail="Models not trained yet")

        predictions = predictor.predict_all(input_data)

        return {"status": "success", "predictions": predictions}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "trained": predictor.is_trained}


if __name__ == "__main__":
    import uvicorn

    print("Starting ML Parameter Analyzer API...")
    print("Initializing models...")
    predictor.load_and_train()
    print("API ready!")
    uvicorn.run(app, host="0.0.0.0", port=5000)
