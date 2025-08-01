# 🚗 ML Parameter Impact Analyzer

Interactive web application that shows how changing one parameter affects all others in real-time using trained ML models.

## Features

- **Real-time Parameter Control**: Adjust any driving parameter with sliders
- **ML-Powered Predictions**: See how all variables respond instantly
- **Beautiful Interface**: Clean, responsive design with Material-UI
- **Full Control**: Change speed, throttle, brake, temperature, etc.

## Quick Start

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Node Dependencies
```bash
npm install
```

### 3. Start the Application

**Terminal 1: Start API Server**
```bash
python api_server.py
```

**Terminal 2: Start Web Interface**
```bash
npm run start
```

The app will open at `http://localhost:3000`

## How It Works

1. **ML Training**: Loads tire wear dataset from Kaggle and trains Random Forest models
2. **Parameter Control**: Web interface with sliders for all driving parameters
3. **Real-time Predictions**: API predicts all variables when you change any parameter
4. **Visual Feedback**: Color-coded values and instant updates

## Example Usage

- Set **Speed to 120 mph** → See how tire wear, temperature, and force change
- Increase **Throttle** → Watch impact on tire degradation  
- Adjust **Surface Roughness** → Observe cumulative wear effects

## Architecture

- **Frontend**: React + Material-UI
- **Backend**: Flask API with trained scikit-learn models
- **ML Models**: Random Forest regressors for each variable
- **Data**: Kaggle tire wear simulation dataset

Perfect for understanding parameter relationships in complex systems!