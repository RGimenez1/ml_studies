"""
Clean Architecture API Server Entry Point.

This is the new entry point using clean architecture principles.
The old api_server.py is kept for reference but this should be used instead.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.main import main

if __name__ == "__main__":
    main()