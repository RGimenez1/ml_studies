"""
Clean Architecture FastAPI Application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from .core.config import AppConfig
from .core.container import Container


def create_app(config: AppConfig) -> FastAPI:
    """Create FastAPI application with clean architecture."""
    
    # Create dependency injection container
    container = Container(config)
    
    # Create FastAPI app
    app = FastAPI(
        title=config.api.title,
        version=config.api.version
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.api.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Get controller
    ml_controller = container.get_ml_controller()
    
    # Register routes
    @app.get("/api/initialize")
    async def initialize():
        """Initialize the ML models."""
        return await ml_controller.initialize()
    
    @app.post("/api/predict")
    async def predict(input_data: dict):
        """Make predictions based on input parameters."""
        return await ml_controller.predict(input_data)
    
    @app.get("/api/health")
    async def health():
        """Health check endpoint."""
        return await ml_controller.health()
    
    return app


def main():
    """Main application entry point."""
    config = AppConfig.from_env()
    app = create_app(config)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting ML Parameter Analyzer API...")
    
    # Initialize models on startup
    container = Container(config)
    model_init_use_case = container.get_model_init_use_case()
    
    try:
        logger.info("Initializing models...")
        model_init_use_case.execute()
        logger.info("API ready!")
    except Exception as e:
        logger.error(f"Failed to initialize models: {e}")
        raise
    
    # Start server
    uvicorn.run(
        app,
        host=config.api.host,
        port=config.api.port
    )


if __name__ == "__main__":
    main()