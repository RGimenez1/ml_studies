import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pathlib
import kagglehub

class ParameterImpactAnalyzer:
    def __init__(self):
        self.data = None
        self.models = {}
        self.feature_columns = []
        self.target_columns = []
        
    def load_data(self):
        """Load and prepare the tire wear dataset"""
        print("Loading dataset...")
        path = kagglehub.dataset_download("samwelnjehia/simple-tire-wear-and-degradation-simulated-dataset")
        DATA_DIR = pathlib.Path(path)
        self.data = pd.read_csv(DATA_DIR / 'simulated_dataset.csv')
        
        # Define key variables we want to analyze
        self.feature_columns = [
            'Speed', 'Throttle', 'Brake', 'Surface_Roughness',
            'front_surface_temp', 'rear_surface_temp', 'force_on_tire'
        ]
        
        self.target_columns = [
            'Tire_wear', 'Tire degreadation', 'cumilative_Tire_Wear'
        ]
        
        print(f"Data loaded: {len(self.data)} samples")
        print(f"Analyzing relationships between {len(self.feature_columns)} inputs and {len(self.target_columns)} outputs")
        
    def train_models(self):
        """Train models to predict each variable from all others"""
        print("Training predictive models...")
        
        # Train a model for each variable to predict it from others
        all_variables = self.feature_columns + self.target_columns
        
        for target_var in all_variables:
            # Use all other variables as features
            feature_vars = [var for var in all_variables if var != target_var]
            
            X = self.data[feature_vars].fillna(0)
            y = self.data[target_var].fillna(0)
            
            # Train random forest model
            model = RandomForestRegressor(n_estimators=50, random_state=42)
            model.fit(X, y)
            
            # Store model and feature names
            self.models[target_var] = {
                'model': model,
                'features': feature_vars,
                'r2_score': r2_score(y, model.predict(X))
            }
            
        print(f"Trained {len(self.models)} models")
        
    def get_correlations(self):
        """Calculate correlation matrix"""
        variables = self.feature_columns + self.target_columns
        correlation_matrix = self.data[variables].corr()
        return correlation_matrix
        
    def analyze_parameter_impact(self, parameter, change_amount):
        """Analyze how changing one parameter affects all others"""
        if parameter not in self.feature_columns + self.target_columns:
            print(f"Parameter '{parameter}' not found!")
            return None
            
        print(f"\\n=== IMPACT ANALYSIS: {parameter} change by {change_amount} ===")
        
        # Get baseline values (median)
        baseline = {}
        for var in self.feature_columns + self.target_columns:
            baseline[var] = self.data[var].median()
            
        # Create modified scenario
        modified = baseline.copy()
        modified[parameter] += change_amount
        
        print(f"\\nBaseline {parameter}: {baseline[parameter]:.2f}")
        print(f"Modified {parameter}: {modified[parameter]:.2f}")
        
        # Predict all variables in both scenarios
        impacts = {}
        
        for target_var in self.models.keys():
            if target_var == parameter:
                # Direct change
                impacts[target_var] = {
                    'baseline': baseline[target_var],
                    'modified': modified[target_var],
                    'change': change_amount,
                    'percent_change': (change_amount / baseline[target_var]) * 100 if baseline[target_var] != 0 else 0
                }
            else:
                # Predict using trained model
                model_info = self.models[target_var]
                model = model_info['model']
                features = model_info['features']
                
                # Prepare feature vectors
                baseline_features = [baseline[f] for f in features]
                modified_features = [modified[f] if f == parameter else baseline[f] for f in features]
                
                # Make predictions
                baseline_pred = model.predict([baseline_features])[0]
                modified_pred = model.predict([modified_features])[0]
                
                change = modified_pred - baseline_pred
                percent_change = (change / baseline_pred) * 100 if baseline_pred != 0 else 0
                
                impacts[target_var] = {
                    'baseline': baseline_pred,
                    'modified': modified_pred,
                    'change': change,
                    'percent_change': percent_change
                }
        
        # Sort by absolute impact
        sorted_impacts = sorted(impacts.items(), 
                              key=lambda x: abs(x[1]['percent_change']), 
                              reverse=True)
        
        print(f"\\nIMPACT RESULTS (sorted by magnitude):")
        print(f"{'Variable':<20} {'Baseline':<10} {'Modified':<10} {'Change':<10} {'% Change':<10}")
        print("-" * 70)
        
        for var_name, impact in sorted_impacts:
            print(f"{var_name:<20} {impact['baseline']:<10.3f} {impact['modified']:<10.3f} "
                  f"{impact['change']:<10.3f} {impact['percent_change']:<10.1f}%")
                  
        return impacts
        
    def correlation_analysis(self, parameter):
        """Show correlations for a specific parameter"""
        corr_matrix = self.get_correlations()
        correlations = corr_matrix[parameter].sort_values(key=abs, ascending=False)
        
        print(f"\\n=== CORRELATIONS WITH {parameter} ===")
        print(f"{'Variable':<25} {'Correlation':<12}")
        print("-" * 40)
        
        for var, corr in correlations.items():
            if var != parameter:
                strength = "Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.3 else "Weak"
                direction = "Positive" if corr > 0 else "Negative"
                print(f"{var:<25} {corr:<12.3f} ({strength} {direction})")
                
    def interactive_analyzer(self):
        """Interactive parameter analysis"""
        print("\\n=== INTERACTIVE PARAMETER ANALYZER ===")
        print("Available parameters:")
        all_vars = self.feature_columns + self.target_columns
        for i, var in enumerate(all_vars, 1):
            print(f"  {i}. {var}")
            
        while True:
            try:
                print("\\nChoose analysis:")
                print("1. Parameter impact analysis")
                print("2. Correlation analysis")
                print("3. Quit")
                
                choice = input("Enter choice (1-3): ").strip()
                
                if choice == '3':
                    break
                elif choice in ['1', '2']:
                    param_input = input(f"Enter parameter name (or number 1-{len(all_vars)}): ").strip()
                    
                    # Handle numeric input
                    if param_input.isdigit():
                        param_idx = int(param_input) - 1
                        if 0 <= param_idx < len(all_vars):
                            parameter = all_vars[param_idx]
                        else:
                            print("Invalid number!")
                            continue
                    else:
                        parameter = param_input
                        
                    if parameter not in all_vars:
                        print(f"Parameter '{parameter}' not found!")
                        continue
                        
                    if choice == '1':
                        change = float(input(f"Enter change amount for {parameter}: "))
                        self.analyze_parameter_impact(parameter, change)
                    else:
                        self.correlation_analysis(parameter)
                        
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    """Main function to run the analyzer"""
    analyzer = ParameterImpactAnalyzer()
    
    # Load data and train models
    analyzer.load_data()
    analyzer.train_models()
    
    # Show model performance
    print("\\nModel Performance (R² scores):")
    for var, info in analyzer.models.items():
        print(f"  {var:<25}: {info['r2_score']:.3f}")
    
    # Example analyses
    print("\\n" + "="*60)
    print("EXAMPLE ANALYSES")
    print("="*60)
    
    # Example 1: What happens if speed increases by 20 mph?
    analyzer.analyze_parameter_impact('Speed', 20)
    
    # Example 2: What happens if tire wear increases by 0.1?
    analyzer.analyze_parameter_impact('Tire_wear', 0.1)
    
    # Example 3: Show correlations with speed
    analyzer.correlation_analysis('Speed')
    
    # Interactive mode
    print("\\n" + "="*60)
    analyzer.interactive_analyzer()
    
    return analyzer

if __name__ == "__main__":
    analyzer = main()