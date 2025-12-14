# api/index.py - Vercel Serverless Handler
from mangum import Mangum
import sys
import os

# Add parent directory to path so we can import from main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the FastAPI app
from main import app as fastapi_app

# Mangum adapter for serverless
handler = Mangum(fastapi_app, lifespan="off")

# Vercel also checks for 'app'
app = handler
