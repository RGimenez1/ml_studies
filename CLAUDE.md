# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a machine learning studies repository focused on tire wear prediction. The project has evolved into a complete full-stack ML application that provides real-time parameter impact analysis.

## Environment Setup

The repository uses a Python virtual environment with the following key dependencies:

- pandas (>=1.5.0) - Data manipulation and analysis
- numpy (>=1.21.0) - Numerical computing
- scikit-learn (>=1.0.0) - Machine learning library
- matplotlib (>=3.5.0) & seaborn (>=0.11.0) - Data visualization
- torch (>=1.12.0) - Deep learning framework
- jupyter (>=1.0.0) - Interactive notebooks
- kagglehub (>=0.1.0) - Kaggle dataset integration
- fastapi (>=0.104.0) - Web API framework
- uvicorn (>=0.24.0) - ASGI server

## 🚀 Quick Start Guide - From Zero to Running Application

Follow these steps to get the complete ML Parameter Impact Analyzer running from scratch:

### Step 1: Prerequisites

Ensure you have the following installed on your system:

- Python 3.8+ (preferably 3.10+)
- Node.js 16+ and npm
- Git (to clone the repository)
- `uv` package manager (install with: `pip install uv`)

### Step 2: Clone and Navigate to Repository

```bash
git clone <repository-url>
cd ml_studies
```

### Step 3: Set Up Python Environment

```bash
# Create virtual environment
uv venv .venv

# Activate virtual environment
source .venv/Scripts/activate  # Windows
# or
source .venv/bin/activate      # Linux/Mac

# Install Python dependencies
uv pip install -r requirements.txt
```

### Step 4: Set Up React Frontend

```bash
# Install React dependencies
npm install
```

### Step 5: Start the Application

**You need TWO terminals running simultaneously:**

**Terminal 1 - API Server:**

```bash
# Activate Python environment
source .venv/Scripts/activate  # Windows
# or
source .venv/bin/activate      # Linux/Mac

# Start FastAPI server
python api_server.py
```

_Server will start on http://localhost:5000_

**Terminal 2 - React Frontend:**

```bash
# Start React development server
npm run start
```

_Frontend will start on http://localhost:3000_

### Step 6: Access Your Application

Open your browser and navigate to: **http://localhost:3000**

You should see the ML Parameter Impact Analyzer with interactive sliders for:

- Speed, Braking Intensity, Throttle Position
- Surface Conditions, Temperature variations
- Real-time tire wear predictions

### ✅ Verification Checklist

- [ ] API health check: http://localhost:5000/api/health returns `{"status":"healthy","trained":true}`
- [ ] Frontend loads: http://localhost:3000 shows the analyzer interface
- [ ] Sliders work and update predictions in real-time
- [ ] No console errors in browser developer tools

### Troubleshooting

- **Python import errors**: Ensure virtual environment is activated and all dependencies installed
- **React build errors**: Delete `node_modules` folder and run `npm install` again
- **API connection issues**: Check that both servers are running on correct ports (5000 and 3000)
- **jsconfig.json errors**: File should contain valid JSON (not comments)

## Common Commands

### Environment Management

```bash
# Install dependencies (use uv pip as specified in project goals)
uv pip install -r requirements.txt

# Activate virtual environment (if not already active)
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### Full-Stack Application

```bash
# Terminal 1: Start API Server
python api_server.py

# Terminal 2: Start Web Interface
npm install  # First time only
npm run start

# Access application at http://localhost:3000
```

### Development Tools

```bash
# Start Jupyter server
jupyter notebook
# or
jupyter lab

# Run Python scripts
python script_name.py

# Train ML models
python simple_ml_model.py
```

## Development Notes

- **Full-Stack ML Application**: Complete web application with React frontend and FastAPI backend
- **Real-Time Predictions**: Interactive parameter control with instant ML-powered predictions
- **Production Ready**: Trained models saved with metadata (trained 2025-07-30)
- **Kaggle Integration**: Uses tire wear simulation dataset via kagglehub
- **Feature Engineering**: Advanced interaction features (speed×brake, throttle×surface, temp_diff)

## Project Goals & Achievements

### ✅ MAJOR BREAKTHROUGH COMPLETED

- **Goal**: Create a working ML model that can predict tire wear and degradation
- **Achievement**: Built complete ML Parameter Impact Analyzer with:
  - 10 trained Random Forest models for real-time predictions
  - Interactive web interface with Material-UI sliders
  - FastAPI backend serving ML predictions
  - Real-time parameter impact visualization
  - Full production deployment capability

### Current Status

- **Models Trained**: ✅ Random Forest regressors for all driving parameters
- **Web Application**: ✅ React frontend with real-time parameter control
- **API Integration**: ✅ FastAPI backend with CORS support
- **Data Pipeline**: ✅ Kaggle dataset integration and preprocessing
- **Feature Engineering**: ✅ Advanced interaction features implemented

### Development Standards

- Never install packages with just 'pip'. Always use 'uv pip' and 'uv pip install'
- Models saved in `saved_models/` directory with metadata tracking
- Always use uv
