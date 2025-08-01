# ML Parameter Impact Analyzer

Professional full-stack ML application for real-time tire wear prediction with clean architecture implementation.

## Quick Start

### Prerequisites

- Python 3.8+ and Node.js 16+
- `uv` package manager: `pip install uv`

### Setup

```bash
# Install dependencies
uv venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
npm install

# Start application
npm run dev

# Open browser
# http://localhost:3000
```

## Application Overview

Complete ML-powered tire wear analysis system with:

- **10 trained Random Forest models** for real-time predictions
- **Interactive parameter control** with Material-UI sliders
- **FastAPI backend** with clean architecture
- **React frontend** with professional UI components
- **Real-time predictions** with debounced API calls

## Architecture

### Backend (Clean Architecture)

- **Domain Layer**: Business entities and interfaces
- **Core Layer**: Use cases and configuration management
- **Infrastructure Layer**: ML training, data access, model persistence
- **API Layer**: FastAPI controllers and routing

### Frontend (Component Architecture)

- **Components**: Reusable UI components
- **Hooks**: State management and custom logic
- **Services**: API communication layer
- **Utils**: Configuration and formatting utilities

## Commands

```bash
npm run dev     # Start both API and frontend
npm run server  # Start API server only
npm start       # Start frontend only
npm run build   # Build for production
```

## Configuration

Environment variables (optional):

- `API_HOST`: API host (default: localhost)
- `API_PORT`: API port (default: 5000)
- `DEV_MODE`: Development mode (default: true)
- `USE_FAST_MODEL`: Use LinearRegression vs RandomForest (default: false)

## Development Standards

- Clean architecture with clear separation of concerns
- Environment-based configuration management
- Professional error handling and logging
- Type-safe interfaces and contracts
- Debounced API calls for optimal performance
- Material-UI design system
- Always use `uv pip` for Python package management

## Project Status

✅ **Production Ready**

- Models trained and cached
- Full-stack application deployed
- Professional UI/UX
- Clean architecture implemented
- Comprehensive error handling
