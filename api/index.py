# api/index.py - Vercel Serverless Handler
import sys
import os

# Add parent directory to path so we can import from main.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

# This is the handler that Vercel will call
handler = app
