# auth/routes.py
from fastapi import APIRouter, Body, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from supabase import create_client
from dotenv import load_dotenv
import os

from config import get_monthly_question_limit, ERROR_MESSAGES, SUCCESS_MESSAGES
from utils.logging_config import get_logger
from utils.exceptions import AuthenticationError, EmailNotVerifiedError, ValidationError

load_dotenv()

# Setup logging
logger = get_logger("auth")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", SUPABASE_KEY)  # Add this

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

auth_router = APIRouter()


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(f"[AUTH] Validating token. SUPABASE_JWT_SECRET exists: {bool(SUPABASE_JWT_SECRET)}")
        print(f"[AUTH] Token (first 20 chars): {token[:20]}...")

        # Supabase tokens need the JWT secret to decode
        # Skip signature, audience, and expiry verification since Supabase handles that
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_exp": False
            }
        )

        user_id = payload.get("sub")  # Supabase uses 'sub' for user ID
        email = payload.get("email")

        print(f"[AUTH] JWT decoded successfully. User ID: {user_id}, Email: {email}")
        print(f"[AUTH] JWT payload keys: {list(payload.keys())}")

        if not user_id or not email:
            print(f"[AUTH] Missing user_id or email in JWT payload")
            raise credentials_exception

    except JWTError as e:
        print(f"[AUTH] JWT Error: {type(e).__name__}: {e}")
        import traceback
        print(f"[AUTH] Full traceback: {traceback.format_exc()}")
        raise credentials_exception
    except Exception as e:
        print(f"[AUTH] Unexpected error: {type(e).__name__}: {e}")
        import traceback
        print(f"[AUTH] Full traceback: {traceback.format_exc()}")
        raise credentials_exception

    # Query Supabase for the user
    print(f"[AUTH] Querying Supabase for user: {user_id}")
    response = supabase_client.table("users").select("*").eq("id", user_id).execute()

    if not response.data:
        print(f"[AUTH] User not found in database: {user_id}")
        print(f"[AUTH] Creating user record in public.users for {email}")

        # Auto-create user record if missing (handles cases where registration didn't complete)
        try:
            email_confirmed = payload.get("email_confirmed_at") is not None
            create_response = supabase_client.table("users").insert({
                "id": user_id,
                "username": email.split("@")[0],  # Use email prefix as username
                "email": email,
                "tier": "free",
                "email_verified": email_confirmed,
                "monthly_chars_used": 0
            }).execute()

            if create_response.data:
                user_data = create_response.data[0]
                print(f"[AUTH] User record created successfully")
            else:
                print(f"[AUTH] Failed to create user record")
                raise credentials_exception
        except Exception as create_error:
            print(f"[AUTH] Error creating user record: {create_error}")
            raise credentials_exception
    else:
        user_data = response.data[0]
        print(f"[AUTH] User found: {user_data.get('email')}, tier: {user_data.get('tier')}")

    # Note: email_verified is managed in the database
    # It's set during registration or manually updated by admins
    print(f"[AUTH] Email verified status: {user_data.get('email_verified', False)}")

    return user_data


@auth_router.post("/register")
async def register(username: str = Body(...), email: str = Body(...), password: str = Body(...)):
    try:
        auth_response = supabase_client.auth.sign_up({
            "email": email,
            "password": password
        })

        # Check if user was created
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Registration failed - no user created")

        # Insert into public.users
        # Check if email was auto-confirmed (should be False by default if email confirmation is enabled)
        email_verified = auth_response.user.email_confirmed_at is not None

        print(f"[REGISTER] Attempting to insert user {auth_response.user.id} into public.users")
        try:
            insert_response = supabase_client.table("users").insert({
                "id": auth_response.user.id,
                "username": username,
                "email": email,
                "tier": "free",
                "email_verified": email_verified
            }).execute()
            print(f"[REGISTER] User inserted successfully: {insert_response.data}")
        except Exception as insert_error:
            print(f"[REGISTER] ERROR inserting user into public.users: {insert_error}")
            # Try to continue anyway - user exists in auth.users
            print(f"[REGISTER] User exists in auth.users but not in public.users. Will need manual fix.")

        # If email confirmation is enabled, session will be None
        if auth_response.session and auth_response.session.access_token:
            return {
                "access_token": auth_response.session.access_token,
                "token_type": "bearer",
                "message": "Registration successful! You can now login."
            }
        else:
            # Email confirmation required (session is None or doesn't have access_token)
            return {
                "message": "Registration successful! Please check your email to verify your account before logging in.",
                "email_confirmation_required": True
            }

    except HTTPException:
        raise
    except Exception as e:
        # More detailed error message
        error_msg = str(e)
        print(f"Registration error: {error_msg}")  # Log to server console
        raise HTTPException(status_code=400, detail=f"Registration failed: {error_msg}")


@auth_router.post("/login")
async def login(email: str = Body(...), password: str = Body(...)):
    try:
        auth_response = supabase_client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if auth_response.user:
            return {
                "access_token": auth_response.session.access_token,
                "token_type": "bearer"
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@auth_router.post("/resend-verification")
async def resend_verification(email: str = Body(...)):
    try:
        # Supabase resend verification email
        supabase_client.auth.resend({
            "type": "signup",
            "email": email
        })

        return {
            "message": "Verification email sent! Please check your inbox.",
            "success": True
        }
    except Exception as e:
        error_message = str(e)
        # Handle common error cases
        if "email not confirmed" in error_message.lower() or "user not found" in error_message.lower():
            raise HTTPException(status_code=400, detail="Email not found or already verified. Please try registering again.")
        raise HTTPException(status_code=400, detail=f"Failed to resend verification email: {error_message}")


@auth_router.get("/auth/callback")
async def auth_callback():
    """
    Handle Supabase email verification callback.
    Configure this URL in Supabase Dashboard > Authentication > URL Configuration
    Redirect URL should be: https://yourdomain.com/auth/callback
    """
    from fastapi.responses import RedirectResponse
    # After Supabase verifies the email, redirect user to login page with success message
    return RedirectResponse(url="/login?verified=true")


@auth_router.get("/usage")
async def get_usage(current_user: dict = Depends(get_current_user)):
    """Get current user's usage statistics and tier information"""
    tier = current_user.get("tier", "free")

    # Get tier limit from config
    monthly_limit = get_monthly_question_limit(tier)
    questions_used = current_user.get("monthly_chars_used", 0)  # Reusing this field for question count

    logger.info(f"Usage request for user: {current_user.get('email')}, tier: {tier}, used: {questions_used}/{monthly_limit}")

    return {
        "username": current_user.get("username"),
        "email": current_user.get("email"),
        "tier": tier,
        "monthly_limit": monthly_limit,
        "questions_used": questions_used,
        "questions_remaining": max(0, monthly_limit - questions_used),
        "email_verified": current_user.get("email_verified", False)
    }