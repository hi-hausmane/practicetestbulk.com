# main.py - FastAPI Application with Auth, Billing, and Test Generation
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# Import routers
from auth.routes import auth_router
from billing.routes import billing_router
from generator.routes import generator_router

# Import config
from config import APP_NAME, APP_DESCRIPTION, APP_VERSION

# Initialize FastAPI app with enhanced metadata
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/api/docs",  # Swagger UI
    redoc_url="/api/redoc",  # ReDoc UI
    openapi_url="/api/openapi.json",
    contact={
        "name": "PracticeTestBulk Support",
        "email": "support@practicetestbulk.com",
    },
    license_info={
        "name": "Proprietary",
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://practicetestbulk.com",
            "description": "Production server"
        }
    ],
    tags_metadata=[
        {
            "name": "Authentication",
            "description": "User authentication and registration endpoints"
        },
        {
            "name": "Billing",
            "description": "Subscription and payment management"
        },
        {
            "name": "Generator",
            "description": "AI-powered practice test question generation"
        },
        {
            "name": "Pages",
            "description": "HTML page endpoints"
        }
    ]
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Register routers
app.include_router(auth_router, tags=["Authentication"])
app.include_router(billing_router, tags=["Billing"])
app.include_router(generator_router, tags=["Generator"])


@app.get("/", response_class=HTMLResponse, tags=["Pages"])
async def landing_page(request: Request):
    """
    Landing Page

    Homepage with product information, features, and demo examples.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/app", response_class=HTMLResponse, tags=["Pages"])
async def app_page(request: Request):
    """
    Test Generator Application

    Main application page for generating practice test questions.
    Requires authentication.
    """
    return templates.TemplateResponse("app.html", {"request": request})


@app.get("/pro", response_class=HTMLResponse, tags=["Pages"])
async def pro_page(request: Request):
    """
    Pricing & Plans Page

    View subscription plans and upgrade options (Free, Pro, Business).
    """
    return templates.TemplateResponse("pro.html", {"request": request})


@app.get("/login", response_class=HTMLResponse, tags=["Pages"])
async def login_page(request: Request):
    """
    Login Page

    User authentication page with email/password and Google OAuth.
    """
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse, tags=["Pages"])
async def register_page(request: Request):
    """
    Registration Page

    Create a new user account with email verification.
    """
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/verify-email", response_class=HTMLResponse, tags=["Pages"])
async def verify_email_page(request: Request):
    """
    Email Verification Page

    Shows email verification instructions and resend options.
    """
    return templates.TemplateResponse("verify-email.html", {"request": request})


@app.get("/health", tags=["System"])
async def health_check():
    """
    Health Check Endpoint

    Returns application health status for monitoring.
    """
    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": APP_VERSION
    }
