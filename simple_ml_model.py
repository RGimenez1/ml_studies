import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pathlib
import kagglehub

def load_data():
    """Load tire wear dataset from Kaggle"""
    print("Downloading dataset...")
    path = kagglehub.dataset_download("samwelnjehia/simple-tire-wear-and-degradation-simulated-dataset")
    print(f"Dataset downloaded to: {path}")
    
    DATA_DIR = pathlib.Path(path)
    df = pd.read_csv(DATA_DIR / 'simulated_dataset.csv')
    print(f"Dataset loaded: {len(df)} rows, {len(df.columns)} columns")
    return df

def preprocess_data(df):
    """Feature engineering and preprocessing"""
    # Create interaction features
    df['speed_x_brake'] = df['Speed'] * df['Brake']
    df['throttle_x_surface'] = df['Throttle'] * df['Surface_Roughness']
    df['temp_diff'] = df['front_surface_temp'] - df['rear_surface_temp']
    
    # Select enhanced features
    features = [
        'Throttle', 'Brake', 'Speed', 'Surface_Roughness',
        'front_surface_temp', 'rear_surface_temp', 'force_on_tire',
        'speed_x_brake', 'throttle_x_surface', 'temp_diff'
    ]
    
    X = df[features].fillna(0)
    y = df['Tire_wear']
    
    return X, y, features

def train_models(X, y):
    """Train and evaluate ML models"""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define models
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
    }
    
    # Train and evaluate
    results = {}
    trained_models = {}
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        results[name] = {
            'R²': r2_score(y_test, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_test, y_pred))
        }
        trained_models[name] = model
    
    return results, trained_models, X_test, y_test

def analyze_feature_importance(model, feature_names):
    """Analyze feature importance for Random Forest"""
    if hasattr(model, 'feature_importances_'):
        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        return importance_df
    return None

def predict_scenarios(model, feature_names):
    """Make predictions for different driving scenarios"""
    scenarios = [
        ("Normal driving", [0.7, 0.1, 120, 1.2, 85, 100, 25000, 12, 0.84, -15]),
        ("Aggressive driving", [1.0, 0.3, 180, 1.4, 110, 120, 40000, 54, 1.4, -10]),
        ("Careful driving", [0.5, 0.05, 80, 1.1, 83, 99, 15000, 4, 0.55, -16]),
        ("Racing conditions", [0.9, 0.4, 200, 1.5, 140, 145, 50000, 80, 1.35, -5])
    ]
    
    predictions = {}
    for name, features in scenarios:
        prediction = model.predict([features])[0]
        predictions[name] = prediction
    
    return predictions

def main():
    """Main ML pipeline"""
    print("=== TIRE WEAR ML MODEL ===\n")
    
    # Load and preprocess data
    df = load_data()
    X, y, feature_names = preprocess_data(df)
    
    # Train models
    results, trained_models, X_test, y_test = train_models(X, y)
    
    # Display results
    print("\nModel Performance:")
    for name, metrics in results.items():
        print(f"  {name:20s}: R² = {metrics['R²']:.4f}, RMSE = {metrics['RMSE']:.4f}")
    
    # Feature importance analysis
    rf_model = trained_models['Random Forest']
    importance_df = analyze_feature_importance(rf_model, feature_names)
    
    if importance_df is not None:
        print("\nTop 5 Most Important Features:")
        for idx, row in importance_df.head().iterrows():
            print(f"  {row['feature']:20s}: {row['importance']:.4f}")
    
    # Scenario predictions
    predictions = predict_scenarios(rf_model, feature_names)
    print("\nScenario Predictions:")
    for scenario, prediction in predictions.items():
        print(f"  {scenario:20s}: {prediction:.4f} tire wear")
    
    print("\n=== MODEL READY FOR USE ===")
    return trained_models, feature_names

if __name__ == "__main__":
    models, features = main()