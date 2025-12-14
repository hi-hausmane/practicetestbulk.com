# Project Structure Documentation

## Overview

TestGenius AI is a FastAPI-based SaaS application that generates Udemy practice test questions using AI. The project follows a modular architecture with clear separation of concerns.

## Directory Tree

```
udemy-practice-test-maker/
│
├── main.py                          # Application entry point, FastAPI app initialization
├── config.py                        # Centralized configuration and constants
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables (git-ignored)
│
├── auth/                           # Authentication Module
│   ├── __init__.py                # Module initialization
│   ├── routes.py                  # Auth endpoints: /register, /login, /usage
│   └── services.py                # Supabase integration, JWT handling
│
├── billing/                        # Billing & Subscription Module
│   ├── __init__.py                # Module initialization
│   ├── routes.py                  # Billing endpoints: /subscribe, /webhook
│   └── services.py                # Stripe integration, webhook handlers
│
├── generator/                      # AI Question Generation Module
│   ├── __init__.py                # Module initialization
│   ├── routes.py                  # Generation endpoint: /generate
│   └── services.py                # AI integration (Claude/DeepSeek), CSV export
│
├── utils/                          # Shared Utilities
│   ├── __init__.py                # Module initialization
│   ├── logging_config.py          # Structured logging setup
│   └── exceptions.py              # Custom exception classes
│
├── static/                         # Frontend Assets
│   ├── css/
│   │   └── udemy-theme.css        # Udemy-inspired design system
│   ├── js/
│   │   ├── pages/                 # Page-specific JavaScript
│   │   │   ├── app.js             # Test generator app logic
│   │   │   ├── pro.js             # Pricing page logic
│   │   │   ├── landing.js         # Homepage interactivity
│   │   │   ├── login.js           # Login form handling
│   │   │   ├── register.js        # Registration handling
│   │   │   └── verify-email.js    # Email verification
│   │   └── utils/                 # Reusable JS utilities
│   │       ├── api-client.js      # Centralized API client
│   │       ├── auth.js            # Auth state management
│   │       └── helpers.js         # UI utility functions
│   └── files/                     # Static files (CSVs, examples)
│
├── templates/                      # Jinja2 HTML Templates
│   ├── components/                # Reusable components
│   │   ├── nav_landing.html       # Landing page navbar
│   │   ├── nav_app.html           # App navbar (authenticated)
│   │   ├── nav_auth.html          # Auth pages navbar
│   │   ├── footer.html            # Footer component
│   │   └── js_utils.html          # Shared JavaScript utilities
│   ├── pages/                     # Full page templates
│   │   ├── index.html             # Landing page
│   │   ├── app.html               # Test generator application
│   │   ├── pro.html               # Pricing & plans
│   │   ├── login.html             # Login page
│   │   ├── register.html          # Registration page
│   │   └── verify-email.html      # Email verification
│   └── base.html                  # Base template (if exists)
│
└── Documentation/                  # Project Documentation
    ├── README.md                  # Main project documentation
    ├── QUICKSTART.md              # Quick setup guide
    ├── ARCHITECTURE.md            # System architecture
    ├── DEVELOPER_GUIDE.md         # Development guide
    ├── DEPLOYMENT_GUIDE.md        # Deployment instructions
    ├── THEME_README.md            # Design system guide
    ├── UDEMY_DESIGN_SYSTEM.md     # Udemy design specifications
    ├── PROJECT_STRUCTURE.md       # This file
    ├── BUSINESS_MODEL.md          # Business logic documentation
    ├── CODE_REFERENCE.md          # Technical code reference
    └── SETUP_GUIDE.md             # Quick initialization guide
```

## Module Breakdown

### Core Application Files

#### `main.py`
- FastAPI application initialization
- Route registration
- Static file mounting
- Template configuration
- OpenAPI documentation setup
- Health check endpoint

**Key Components:**
```python
app = FastAPI(...)           # App with metadata
app.mount("/static", ...)    # Static files
templates = Jinja2Templates  # HTML templates
app.include_router(...)      # Module routers
```

#### `config.py`
- Centralized configuration
- Tier limits and pricing
- Course categories
- Question types
- Difficulty levels
- API settings
- Validation constraints
- Error/success messages

**Key Constants:**
```python
TIER_LIMITS                  # Subscription tier configuration
STRIPE_PRICE_IDS             # Stripe price IDs
COURSE_CATEGORIES            # Available course categories
QUESTION_TYPES               # Supported question formats
DIFFICULTY_LEVELS            # Question difficulty options
AI_PROVIDER                  # "claude" or "deepseek"
VALIDATION                   # Input validation rules
```

### Authentication Module (`auth/`)

**Purpose:** User registration, login, email verification, usage tracking

#### `auth/routes.py`
**Endpoints:**
- `POST /register` - Create new user account
- `POST /login` - Authenticate user, return JWT token
- `GET /usage` - Get user tier and monthly usage stats

**Request/Response Models:**
- `RegisterRequest`: email, password, username
- `LoginRequest`: email, password
- `LoginResponse`: access_token, token_type, user
- `UsageResponse`: tier, questions_used, questions_limit, percentage_used

#### `auth/services.py`
**Functions:**
- `create_user()` - Register user in Supabase
- `verify_credentials()` - Authenticate user
- `get_user_usage()` - Get usage statistics
- `check_usage_limit()` - Enforce monthly limits
- `increment_usage()` - Track question generation

**Dependencies:**
- Supabase Python SDK
- JWT token handling
- Password hashing (handled by Supabase)

### Billing Module (`billing/`)

**Purpose:** Stripe integration, subscription management, webhook handling

#### `billing/routes.py`
**Endpoints:**
- `POST /subscribe` - Create Stripe checkout session
- `POST /webhook` - Handle Stripe webhook events

**Request/Response Models:**
- `SubscribeRequest`: price_id, tier
- `SubscribeResponse`: checkout_url, session_id

#### `billing/services.py`
**Functions:**
- `create_checkout_session()` - Initialize Stripe checkout
- `handle_webhook()` - Process Stripe events
- `update_user_tier()` - Update user subscription tier
- `cancel_subscription()` - Handle cancellations

**Stripe Events Handled:**
- `checkout.session.completed` - Subscription started
- `customer.subscription.updated` - Plan changed
- `customer.subscription.deleted` - Subscription cancelled
- `invoice.payment_failed` - Payment issues

### Generator Module (`generator/`)

**Purpose:** AI-powered question generation, CSV export

#### `generator/routes.py`
**Endpoints:**
- `POST /generate` - Generate practice test questions

**Request Model:**
```python
GenerateRequest:
  - num_questions: int (1-250)
  - working_title: str (max 100 chars)
  - target_audience: str (optional)
  - learning_objectives: List[str] (4-10 items)
  - difficulty: str (beginner/intermediate/advanced/mixed)
  - course_category: str (from COURSE_CATEGORIES)
  - question_type: str (optional, from QUESTION_TYPES)
  - explanation_style: str (optional, from EXPLANATION_STYLES)
```

**Response:**
- CSV file download (Udemy bulk import format)
- Content-Type: text/csv
- Content-Disposition: attachment; filename="test.csv"

#### `generator/services.py`
**Functions:**
- `generate_questions()` - Call AI API (Claude or DeepSeek)
- `format_prompt()` - Build AI prompt from request data
- `parse_ai_response()` - Extract questions from AI output
- `export_to_csv()` - Convert questions to Udemy CSV format
- `validate_questions()` - Ensure quality and format

**AI Integration:**
- Claude API: `anthropic` Python SDK
- DeepSeek API: `openai` SDK (OpenAI-compatible)
- Configurable via `AI_PROVIDER` in config.py

**CSV Format:**
```csv
Question,Question Type,Answer 1,Answer 2,Answer 3,Answer 4,
Correct Answer,Explanation,Domain,Category
```

### Utilities Module (`utils/`)

#### `utils/logging_config.py`
**Purpose:** Structured logging configuration

**Features:**
- JSON-formatted logs
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request ID tracking
- Sensitive data filtering

**Usage:**
```python
from utils.logging_config import get_logger
logger = get_logger(__name__)
logger.info("User registered", user_id=user_id)
```

#### `utils/exceptions.py`
**Purpose:** Custom exception classes

**Exception Classes:**
- `AuthenticationError` - Auth failures
- `UsageLimitError` - Quota exceeded
- `PaymentError` - Billing issues
- `GenerationError` - AI generation failures
- `ValidationError` - Input validation errors

**Usage:**
```python
from utils.exceptions import UsageLimitError
if usage >= limit:
    raise UsageLimitError("Monthly limit reached")
```

### Static Assets (`static/`)

#### `static/css/udemy-theme.css`
**Features:**
- Udemy-inspired color palette
- Typography system
- Button styles
- Form components
- Card layouts
- Responsive grid system
- Dark mode support (optional)

**CSS Variables:**
```css
--udemy-purple: #a435f0
--udemy-gray: #1c1d1f
--button-primary: #a435f0
--button-hover: #8710d8
```

#### `static/js/pages/`
**Page-specific JavaScript files:**

**app.js** - Test generator application
- Form handling for test generation
- File upload (if applicable)
- CSV download handling
- Usage display
- Error handling

**pro.js** - Pricing page
- Plan selection
- Checkout flow
- Stripe integration (frontend)
- Feature comparison

**landing.js** - Homepage
- Hero section animations
- Feature showcases
- Demo examples
- CTA buttons

**login.js** - Login page
- Login form submission
- Google OAuth button
- Error display
- Redirect after login

**register.js** - Registration page
- Registration form
- Password validation
- Email verification trigger
- Error handling

**verify-email.js** - Email verification
- Resend email button
- Status checking
- Auto-redirect after verification

#### `static/js/utils/`
**Reusable JavaScript utilities:**

**api-client.js** - Centralized API client
```javascript
class APIClient {
  async post(endpoint, data) { ... }
  async get(endpoint) { ... }
  setAuthToken(token) { ... }
}
```

**auth.js** - Auth state management
```javascript
- getToken() - Retrieve JWT from localStorage
- setToken(token) - Store JWT
- clearToken() - Logout
- isAuthenticated() - Check auth status
- getUserData() - Get user info from token
```

**helpers.js** - UI utility functions
```javascript
- showNotification(message, type)
- showLoading(show)
- formatNumber(num)
- validateEmail(email)
- handleError(error)
```

### Templates (`templates/`)

#### Component Templates (`templates/components/`)

**nav_landing.html** - Landing page navbar
- Logo
- Navigation links (Features, Pricing, Login)
- CTA button (Get Started)

**nav_app.html** - Authenticated app navbar
- Logo
- User menu
- Usage indicator
- Logout button

**nav_auth.html** - Auth pages navbar
- Logo
- Back to home link

**footer.html** - Site footer
- Links (About, Contact, Terms, Privacy)
- Social media
- Copyright

**js_utils.html** - Shared JavaScript
- API client initialization
- Auth helpers
- Common utilities

#### Page Templates (`templates/pages/`)

**index.html** - Landing page
- Hero section
- Features showcase
- Pricing preview
- Demo examples
- Call-to-action

**app.html** - Test generator application
- Generation form
- Course information inputs
- Learning objectives
- Generation button
- Usage display
- Download area

**pro.html** - Pricing & plans
- Three-tier comparison (Free, Pro, Business)
- Feature lists
- Checkout buttons
- FAQ section

**login.html** - Login page
- Email/password form
- Google OAuth button
- "Forgot password" link
- "Create account" link

**register.html** - Registration page
- Registration form
- Email verification notice
- "Already have account" link

**verify-email.html** - Email verification
- Verification instructions
- Resend email button
- Status messages

## Data Flow

### User Registration Flow
1. User submits registration form (register.html → register.js)
2. POST /register (auth/routes.py)
3. create_user() creates account in Supabase (auth/services.py)
4. Supabase sends verification email
5. User redirected to verify-email.html
6. User clicks link in email → Supabase verifies email
7. User can now log in

### Login Flow
1. User submits login form (login.html → login.js)
2. POST /login (auth/routes.py)
3. verify_credentials() checks Supabase (auth/services.py)
4. JWT token generated and returned
5. Token stored in localStorage (auth.js)
6. User redirected to /app

### Question Generation Flow
1. User fills out generation form (app.html → app.js)
2. POST /generate with auth token (generator/routes.py)
3. Check usage limits (auth/services.py)
4. Call AI API (Claude or DeepSeek) (generator/services.py)
5. Parse AI response into questions
6. Convert to Udemy CSV format (generator/services.py)
7. Increment user usage (auth/services.py)
8. Return CSV file for download
9. Browser triggers CSV download (app.js)

### Subscription Flow
1. User clicks "Upgrade" on pro.html
2. POST /subscribe (billing/routes.py)
3. create_checkout_session() creates Stripe session (billing/services.py)
4. User redirected to Stripe checkout
5. User completes payment
6. Stripe sends webhook to POST /webhook
7. handle_webhook() updates user tier (billing/services.py)
8. User redirected back to app with new tier

## Environment Configuration

### Required Environment Variables

**Supabase (Authentication):**
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key-here
SUPABASE_JWT_SECRET=your-jwt-secret-here
```

**AI Services:**
```bash
# For Claude AI
ANTHROPIC_API_KEY=sk-ant-your-key-here

# For DeepSeek AI
DEEPSEEK_API_KEY=sk-your-key-here
```

**Stripe (Billing):**
```bash
STRIPE_SECRET_KEY=sk_test_your-key-here
STRIPE_PRICE_ID_PRO=price_your-pro-price-id
STRIPE_PRICE_ID_BUSINESS=price_your-business-price-id
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret
```

**Application:**
```bash
BASE_URL=http://localhost:8000
```

## Technology Stack

### Backend
- **FastAPI** - Web framework
- **Python 3.8+** - Programming language
- **Supabase** - Authentication & database
- **Stripe** - Payment processing
- **Claude AI / DeepSeek** - Question generation
- **Uvicorn** - ASGI server

### Frontend
- **Vanilla JavaScript** - No framework
- **Jinja2** - HTML templating
- **Custom CSS** - Udemy-inspired design
- **Fetch API** - HTTP client

### Dependencies (from requirements.txt)
```txt
fastapi
uvicorn[standard]
supabase
stripe
anthropic
openai
python-dotenv
pydantic
jinja2
```

## Key Design Principles

1. **Modularity** - Features organized in separate modules
2. **Separation of Concerns** - Routes, services, utilities separated
3. **DRY** - Configuration centralized in config.py
4. **Security** - JWT auth, environment variables, webhook verification
5. **Scalability** - Modular structure allows easy expansion
6. **Maintainability** - Clear structure, comprehensive documentation

## File Naming Conventions

- **Python files**: lowercase with underscores (snake_case)
  - `auth_routes.py`, `logging_config.py`

- **HTML templates**: lowercase with hyphens (kebab-case)
  - `verify-email.html`, `nav-landing.html`

- **JavaScript files**: lowercase with hyphens (kebab-case)
  - `api-client.js`, `verify-email.js`

- **CSS files**: lowercase with hyphens (kebab-case)
  - `udemy-theme.css`

- **Documentation**: UPPERCASE with underscores
  - `README.md`, `DEVELOPER_GUIDE.md`

## Import Structure

### Python Imports
```python
# Standard library
from typing import Dict, Any
import os

# Third-party packages
from fastapi import FastAPI, Request
from supabase import create_client

# Local modules
from config import TIER_LIMITS
from auth.services import verify_credentials
from utils.logging_config import get_logger
```

### JavaScript Imports
```javascript
// ES6 imports (if using modules)
import { APIClient } from './utils/api-client.js';
import { getToken, setToken } from './utils/auth.js';
import { showNotification } from './utils/helpers.js';
```

## Next Steps

For more information, see:
- **[BUSINESS_MODEL.md](BUSINESS_MODEL.md)** - Business logic and monetization
- **[CODE_REFERENCE.md](CODE_REFERENCE.md)** - Technical API reference
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Quick initialization guide
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Development workflows
