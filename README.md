# ML Parameter Impact Analyzer

Professional full-stack machine learning application for real-time tire wear prediction and analysis.

## Features

- **Real-time ML Predictions**: 10 trained Random Forest models
- **Interactive Interface**: Material-UI sliders for parameter control
- **Clean Architecture**: Professional separation of concerns
- **Production Ready**: Optimized build, error handling, logging

## Quick Start

```bash
# Install dependencies
uv venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
npm install

# Start application
npm run dev

# Open http://localhost:3000
```

## Architecture

**Backend**: Clean Architecture with Domain, Core, Infrastructure, and API layers  
**Frontend**: Component-based React with custom hooks and services  
**ML Pipeline**: Kaggle dataset integration with scikit-learn models  

## Technology Stack

- **Backend**: FastAPI, scikit-learn, pandas, uvicorn
- **Frontend**: React, Material-UI, Axios
- **ML**: Random Forest, Linear Regression, Kaggle datasets
- **Architecture**: Clean Architecture, Dependency Injection

## Commands

- `npm run dev` - Start full application
- `npm run server` - API server only
- `npm start` - Frontend only
- `npm run build` - Production build

Built with clean architecture principles and professional development standards.