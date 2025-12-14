# TestGenius AI - Developer Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Project Structure](#project-structure)
4. [Code Style Guidelines](#code-style-guidelines)
5. [Adding New Features](#adding-new-features)
6. [Working with the Database](#working-with-the-database)
7. [Frontend Development](#frontend-development)
8. [API Development](#api-development)
9. [Testing](#testing)
10. [Debugging](#debugging)
11. [Common Development Tasks](#common-development-tasks)
12. [Troubleshooting](#troubleshooting)
13. [Git Workflow](#git-workflow)
14. [Best Practices](#best-practices)

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git
- A text editor or IDE (VS Code recommended)
- Supabase account (free tier available)
- Anthropic API key (Claude AI)
- Stripe account (for payment testing)

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/udemy-practice-test-maker.git
cd udemy-practice-test-maker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor

# Run the development server
uvicorn main:app --reload

# Access the application
# http://localhost:8000
```

---

## Development Environment Setup

### 1. Python Virtual Environment

**Why**: Isolates project dependencies from system Python.

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Verify activation
which python  # Should show path to venv/bin/python
```

### 2. Environment Variables

Create `.env` file in project root:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-key-here

# Anthropic Claude AI
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your-key-here
STRIPE_PUBLISHABLE_KEY=pk_test_your-key-here
STRIPE_WEBHOOK_SECRET=whsec_your-webhook-secret

# Stripe Price IDs
STRIPE_PRO_PRICE_ID=price_your-pro-price-id
STRIPE_BUSINESS_PRICE_ID=price_your-business-price-id

# Application Settings
APP_ENV=development
LOG_LEVEL=DEBUG
```

**Getting API Keys**:
- **Supabase**: https://supabase.com/dashboard → Your Project → Settings → API
- **Anthropic**: https://console.anthropic.com/ → Account → API Keys
- **Stripe**: https://dashboard.stripe.com/test/apikeys

### 3. IDE Setup (VS Code)

**Recommended Extensions**:
- Python (Microsoft)
- Pylance
- FastAPI Snippets
- Jinja (HTML templating)
- ESLint (JavaScript linting)

**VS Code Settings** (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.analysis.typeCheckingMode": "basic",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.tabSize": 4
  },
  "[javascript]": {
    "editor.tabSize": 2
  }
}
```

### 4. Database Setup (Supabase)

1. Create a Supabase project at https://supabase.com
2. Create required tables:

```sql
-- Users table (handled by Supabase Auth, but we add custom fields)
ALTER TABLE auth.users ADD COLUMN tier TEXT DEFAULT 'free';
ALTER TABLE auth.users ADD COLUMN monthly_chars_used INTEGER DEFAULT 0;
ALTER TABLE auth.users ADD COLUMN username TEXT UNIQUE;

-- Subscriptions table
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  tier TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Usage tracking table
CREATE TABLE usage_tracking (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  questions_generated INTEGER NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  course_title TEXT
);
```

---

## Project Structure

```
udemy-practice-test-maker/
├── auth/                    # Authentication module
│   ├── routes.py           # API endpoints
│   └── services.py         # Business logic
├── billing/                # Billing module
│   ├── routes.py           # Stripe endpoints
│   └── services.py         # Stripe integration
├── generator/              # AI generation module
│   ├── routes.py           # Generation endpoints
│   └── services.py         # Claude AI integration
├── utils/                  # Shared utilities
│   ├── logging_config.py   # Logging setup
│   └── exceptions.py       # Custom exceptions
├── static/                 # Static assets
│   ├── css/               # Stylesheets
│   └── js/                # JavaScript
│       ├── pages/         # Page-specific scripts
│       └── utils/         # Shared utilities
├── templates/              # HTML templates
│   └── components/        # Reusable components
├── main.py                 # FastAPI app entry point
├── config.py              # Configuration constants
└── requirements.txt       # Python dependencies
```

### Module Responsibilities

- **auth/**: User registration, login, JWT validation
- **billing/**: Stripe checkout, webhooks, tier management
- **generator/**: AI prompt building, CSV generation
- **utils/**: Shared code (logging, exceptions, helpers)
- **config.py**: All constants (tier limits, validation rules, etc.)

---

## Code Style Guidelines

### Python Style (PEP 8)

```python
# Good: Clear function names, type hints, docstrings
def get_monthly_question_limit(tier: str) -> int:
    """
    Get the monthly question limit for a given tier.

    Args:
        tier: User's subscription tier (free/pro/business)

    Returns:
        Monthly question limit as integer
    """
    return TIER_LIMITS.get(tier, {}).get("questions_per_month", 20)

# Bad: No type hints, unclear name, no docstring
def get_limit(t):
    return TIER_LIMITS.get(t, {}).get("questions_per_month", 20)
```

**Key Principles**:
- Use 4 spaces for indentation (no tabs)
- Max line length: 100 characters
- Function names: `lowercase_with_underscores`
- Class names: `PascalCase`
- Constants: `UPPERCASE_WITH_UNDERSCORES`
- Always add type hints for function parameters and returns
- Add docstrings to all functions and classes

### JavaScript Style

```javascript
// Good: Consistent formatting, clear names
async function generateTest(formData) {
  try {
    const response = await api.post('/generate', formData);
    return response;
  } catch (error) {
    console.error('Generation failed:', error);
    throw error;
  }
}

// Bad: Inconsistent, unclear
async function genTest(d){
try{
let r=await api.post('/generate',d)
return r
}catch(e){console.log(e);throw e}}
```

**Key Principles**:
- Use 2 spaces for indentation
- Use `const` and `let`, not `var`
- Prefer arrow functions for callbacks
- Use async/await over raw promises
- Add JSDoc comments for complex functions
- Semicolons required

### HTML/Template Style

```html
<!-- Good: Proper indentation, semantic HTML -->
<div class="udemy-card-elevated" style="padding: 48px;">
  <h1 class="udemy-h2">Welcome</h1>
  <p class="udemy-body">Create practice tests with AI</p>
  <button class="udemy-btn udemy-btn-primary">Get Started</button>
</div>

<!-- Bad: No structure, inline styles everywhere -->
<div style="padding:48px;box-shadow:0 4px 6px rgba(0,0,0,0.1)">
<h1 style="font-size:2rem">Welcome</h1><p>Create practice tests with AI</p>
<button style="background:#5624d0;color:white">Get Started</button></div>
```

---

## Adding New Features

### 1. Creating a New API Endpoint

**Example**: Add a "favorites" feature to save generated tests.

**Step 1**: Define the data model (Supabase)
```sql
CREATE TABLE favorites (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  course_title TEXT NOT NULL,
  questions JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Step 2**: Create service function (`favorites/services.py`)
```python
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_SERVICE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def save_favorite(user_id: str, course_title: str, questions: list) -> dict:
    """Save a test to user's favorites."""
    result = supabase.table("favorites").insert({
        "user_id": user_id,
        "course_title": course_title,
        "questions": questions
    }).execute()
    return result.data[0]

def get_favorites(user_id: str) -> list:
    """Get all favorites for a user."""
    result = supabase.table("favorites")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("created_at", desc=True)\
        .execute()
    return result.data
```

**Step 3**: Create route (`favorites/routes.py`)
```python
from fastapi import APIRouter, Depends
from auth.services import get_current_user
from .services import save_favorite, get_favorites

favorites_router = APIRouter(prefix="/favorites")

@favorites_router.post("/", tags=["Favorites"])
async def create_favorite(
    course_title: str,
    questions: list,
    current_user: dict = Depends(get_current_user)
):
    """Save a test to favorites."""
    favorite = save_favorite(
        user_id=current_user["id"],
        course_title=course_title,
        questions=questions
    )
    return {"success": True, "favorite": favorite}

@favorites_router.get("/", tags=["Favorites"])
async def list_favorites(current_user: dict = Depends(get_current_user)):
    """Get user's saved favorites."""
    favorites = get_favorites(current_user["id"])
    return {"favorites": favorites}
```

**Step 4**: Register router in `main.py`
```python
from favorites.routes import favorites_router

app.include_router(favorites_router, tags=["Favorites"])
```

**Step 5**: Add frontend functionality (`static/js/pages/app.js`)
```javascript
async function saveFavorite() {
  const courseTitle = document.getElementById('working-title').value;
  const questions = currentGeneratedQuestions; // Store this after generation

  try {
    const response = await api.post('/favorites/', {
      course_title: courseTitle,
      questions: questions
    });

    showStatus('Test saved to favorites!', 'success');
  } catch (error) {
    showStatus('Failed to save favorite', 'error');
  }
}
```

### 2. Adding a New Configuration Option

**Step 1**: Add to `config.py`
```python
# Question difficulty presets
DIFFICULTY_SETTINGS = {
    "beginner": {
        "complexity": "simple",
        "terminology": "basic",
        "explanation_depth": "detailed"
    },
    "intermediate": {
        "complexity": "moderate",
        "terminology": "industry-standard",
        "explanation_depth": "concise"
    },
    "advanced": {
        "complexity": "complex",
        "terminology": "advanced",
        "explanation_depth": "brief"
    }
}
```

**Step 2**: Use in service
```python
from config import DIFFICULTY_SETTINGS

def build_prompt(request_data):
    difficulty = request_data.get("difficulty", "intermediate")
    settings = DIFFICULTY_SETTINGS[difficulty]

    prompt = f"""
    Generate questions with {settings['complexity']} complexity,
    using {settings['terminology']} terminology.
    Explanations should be {settings['explanation_depth']}.
    """
    return prompt
```

---

## Working with the Database

### Supabase Client Usage

**Import**:
```python
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_SERVICE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
```

**Common Operations**:

```python
# Insert
result = supabase.table("usage_tracking").insert({
    "user_id": user_id,
    "questions_generated": 10,
    "course_title": "AWS Solutions Architect"
}).execute()

# Select
result = supabase.table("users")\
    .select("*")\
    .eq("email", "user@example.com")\
    .single()\
    .execute()

# Update
result = supabase.table("users")\
    .update({"tier": "pro"})\
    .eq("id", user_id)\
    .execute()

# Delete
result = supabase.table("favorites")\
    .delete()\
    .eq("id", favorite_id)\
    .execute()

# Complex query with joins
result = supabase.table("subscriptions")\
    .select("*, users!inner(email, username)")\
    .eq("status", "active")\
    .execute()
```

**Error Handling**:
```python
from utils.exceptions import DatabaseError

try:
    result = supabase.table("users").select("*").execute()
    if not result.data:
        raise DatabaseError("No users found")
    return result.data
except Exception as e:
    logger.error(f"Database error: {str(e)}")
    raise DatabaseError(f"Failed to fetch users: {str(e)}")
```

---

## Frontend Development

### Using the API Client

**Location**: `static/js/utils/api-client.js`

```javascript
// GET request
const userData = await api.get('/usage');

// POST request
const result = await api.post('/generate', {
  num_questions: 10,
  working_title: 'Python Basics',
  learning_objectives: ['Understand variables', 'Use functions']
});

// Download file (CSV)
const blob = await api.downloadFile('/generate', formData);
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'test.csv';
a.click();
```

### Authentication Helpers

**Location**: `static/js/utils/auth.js`

```javascript
// Check if user is logged in
if (!Auth.isAuthenticated()) {
  window.location.href = '/login';
}

// Protect a page
Auth.requireAuth(); // Redirects to /login if not authenticated

// Logout
Auth.logout('/'); // Removes token and redirects
```

### UI Helpers

**Location**: `static/js/utils/helpers.js`

```javascript
// Show status message
showStatus('Test generated successfully!', 'success', 5000);
showStatus('An error occurred', 'error');

// Button loading state
const button = document.getElementById('submit-btn');
setButtonLoading(button, true, 'Generating...');
// ... after operation
setButtonLoading(button, false, 'Generate Test');

// Sanitize filename
const filename = sanitizeFilename('My Course: Part 1');
// Result: "my_course_part_1"
```

### Adding a New Page

**Step 1**: Create HTML template (`templates/my-page.html`)
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>My New Page - TestGenius AI</title>
  <link rel="stylesheet" href="/static/css/udemy-theme.css">
</head>
<body>
  {% include "components/nav_app.html" %}

  <div class="udemy-container" style="padding: 40px 0;">
    <h1 class="udemy-h1">My New Feature</h1>
    <!-- Your content here -->
  </div>

  <script src="/static/js/pages/my-page.js"></script>
</body>
</html>
```

**Step 2**: Create JavaScript (`static/js/pages/my-page.js`)
```javascript
// Page initialization
document.addEventListener('DOMContentLoaded', async () => {
  // Require authentication
  if (!Auth.requireAuth()) return;

  // Load initial data
  await loadData();
});

async function loadData() {
  try {
    const data = await api.get('/my-endpoint');
    renderData(data);
  } catch (error) {
    showStatus('Failed to load data', 'error');
  }
}
```

**Step 3**: Add route in `main.py`
```python
@app.get("/my-page", response_class=HTMLResponse, tags=["Pages"])
async def my_page(request: Request):
    """My New Feature Page"""
    return templates.TemplateResponse("my-page.html", {"request": request})
```

---

## API Development

### Request Validation

**Using Pydantic Models**:
```python
from pydantic import BaseModel, Field, validator

class GenerateTestRequest(BaseModel):
    num_questions: int = Field(..., ge=1, le=50)
    working_title: str = Field(..., min_length=3, max_length=100)
    learning_objectives: list[str] = Field(..., min_items=4, max_items=10)
    difficulty: str = Field(default="intermediate")

    @validator('difficulty')
    def validate_difficulty(cls, v):
        allowed = ['beginner', 'intermediate', 'advanced']
        if v not in allowed:
            raise ValueError(f'Difficulty must be one of {allowed}')
        return v
```

### Error Handling

**Using Custom Exceptions**:
```python
from utils.exceptions import UsageLimitError, ValidationError
from fastapi import HTTPException

@generator_router.post("/generate")
async def generate_test(request: GenerateTestRequest):
    # Check usage limit
    if user_usage >= monthly_limit:
        raise UsageLimitError("Monthly question limit reached")

    # Validate input
    if len(request.learning_objectives) < 4:
        raise ValidationError("At least 4 learning objectives required")

    try:
        result = generate_questions(request)
        return result
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Generation failed")
```

### Logging

```python
from utils.logging_config import get_logger

logger = get_logger("generator")

@generator_router.post("/generate")
async def generate_test(request: GenerateTestRequest):
    logger.info(f"Generating {request.num_questions} questions for: {request.working_title}")

    try:
        result = generate_questions(request)
        logger.info(f"Successfully generated {len(result)} questions")
        return result
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}", exc_info=True)
        raise
```

---

## Testing

### Unit Tests (To Be Implemented)

**Example test structure** (`tests/test_generator.py`):
```python
import pytest
from generator.services import build_prompt, parse_claude_response

def test_build_prompt():
    """Test prompt generation."""
    request_data = {
        "num_questions": 10,
        "working_title": "Python Basics",
        "learning_objectives": ["Variables", "Functions", "Loops", "Lists"]
    }

    prompt = build_prompt(request_data)

    assert "Python Basics" in prompt
    assert "10" in prompt
    assert "Variables" in prompt

def test_parse_claude_response():
    """Test parsing Claude AI response."""
    mock_response = {
        "content": [{
            "text": '{"questions": [{"question": "What is Python?"}]}'
        }]
    }

    result = parse_claude_response(mock_response)

    assert "questions" in result
    assert len(result["questions"]) == 1
```

**Run tests**:
```bash
# Install pytest
pip install pytest

# Run all tests
pytest

# Run specific test file
pytest tests/test_generator.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Manual API Testing

**Using curl**:
```bash
# Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Generate test (with token)
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "num_questions": 5,
    "working_title": "JavaScript Basics",
    "learning_objectives": ["Variables", "Functions", "Arrays", "Objects"],
    "difficulty": "beginner"
  }' \
  --output test.csv
```

**Using Swagger UI**:
1. Start server: `uvicorn main:app --reload`
2. Open: http://localhost:8000/api/docs
3. Expand endpoint
4. Click "Try it out"
5. Fill in parameters
6. Click "Execute"

---

## Debugging

### Python Debugging

**Using print statements**:
```python
@generator_router.post("/generate")
async def generate_test(request: GenerateTestRequest):
    print(f"DEBUG: Request data: {request.dict()}")
    result = generate_questions(request)
    print(f"DEBUG: Generated {len(result)} questions")
    return result
```

**Using Python debugger (pdb)**:
```python
import pdb

@generator_router.post("/generate")
async def generate_test(request: GenerateTestRequest):
    pdb.set_trace()  # Execution will pause here
    result = generate_questions(request)
    return result
```

**VS Code debugger** (`.vscode/launch.json`):
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload"
      ],
      "jinja": true
    }
  ]
}
```

### Frontend Debugging

**Browser DevTools**:
```javascript
// Console logging
console.log('User data:', userData);
console.error('API call failed:', error);

// Debugger statement
async function generateTest() {
  debugger; // Browser will pause here
  const result = await api.post('/generate', formData);
  return result;
}

// Network inspection
// Open DevTools → Network tab → Filter by "Fetch/XHR"
```

---

## Common Development Tasks

### 1. Add a New Tier

**Step 1**: Update `config.py`
```python
TIER_LIMITS = {
    "free": {"questions_per_month": 20, "price_monthly": 0},
    "pro": {"questions_per_month": 2500, "price_monthly": 9},
    "business": {"questions_per_month": 7500, "price_monthly": 19},
    "enterprise": {"questions_per_month": 50000, "price_monthly": 99}  # NEW
}
```

**Step 2**: Update `templates/pro.html` with new pricing card

**Step 3**: Create Stripe price in dashboard

**Step 4**: Add price ID to `.env`
```bash
STRIPE_ENTERPRISE_PRICE_ID=price_xxxxxxxxxxxxx
```

### 2. Change AI Model

**Update `config.py`**:
```python
# From:
AI_MODEL = "claude-3-5-sonnet-20241022"

# To:
AI_MODEL = "claude-3-opus-20240229"  # More powerful, higher cost
```

### 3. Add a New Course Category

**Update `config.py`**:
```python
COURSE_CATEGORIES = [
    "Development",
    "IT & Software",
    "Business",
    "Finance & Accounting",
    "Design",
    "Marketing",
    "Health & Fitness",
    "Photography",  # NEW
    "Music"  # NEW
]
```

**Update frontend form** (`templates/app.html`):
```html
<select id="course-category" class="udemy-input">
  <option value="Development">Development</option>
  <!-- ... -->
  <option value="Photography">Photography</option>
  <option value="Music">Music</option>
</select>
```

### 4. Reset Monthly Usage (Cron Job)

**Create script** (`scripts/reset_monthly_usage.py`):
```python
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_SERVICE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def reset_all_users_usage():
    """Reset monthly_chars_used to 0 for all users."""
    result = supabase.table("users")\
        .update({"monthly_chars_used": 0})\
        .neq("id", "00000000-0000-0000-0000-000000000000")\
        .execute()

    print(f"Reset usage for {len(result.data)} users")

if __name__ == "__main__":
    reset_all_users_usage()
```

**Schedule with cron** (Linux):
```bash
# Run on 1st of every month at midnight
0 0 1 * * cd /path/to/project && /path/to/venv/bin/python scripts/reset_monthly_usage.py
```

---

## Troubleshooting

### Common Errors

**1. "ModuleNotFoundError: No module named 'X'"**
```bash
# Solution: Install missing dependency
pip install module-name

# Or reinstall all dependencies
pip install -r requirements.txt
```

**2. "Supabase error: Invalid API key"**
```bash
# Solution: Check .env file
# Ensure SUPABASE_URL and SUPABASE_ANON_KEY are correct
# Get from: https://supabase.com/dashboard → Your Project → Settings → API
```

**3. "401 Unauthorized" on protected endpoints**
```javascript
// Solution: Check token is being sent
// Open DevTools → Network → Headers
// Should see: Authorization: Bearer <token>

// If missing, check:
localStorage.getItem('access_token')  // Should return token

// If null, user needs to login again
```

**4. "CORS error" in browser console**
```python
# Solution: Add allowed origin in main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**5. "Stripe webhook signature verification failed"**
```bash
# Solution: Use Stripe CLI for local testing
stripe listen --forward-to localhost:8000/webhook

# Copy webhook signing secret to .env
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx
```

### Debugging Checklist

- [ ] Is the virtual environment activated?
- [ ] Are all dependencies installed?
- [ ] Is the `.env` file present with correct values?
- [ ] Is the server running (`uvicorn main:app --reload`)?
- [ ] Are there any error messages in the terminal?
- [ ] Are there any errors in browser console (F12)?
- [ ] Is the database accessible (Supabase)?
- [ ] Are API keys valid and not expired?
- [ ] Is the correct port being used (8000)?

---

## Git Workflow

### Branch Strategy

```bash
# Main branches
main          # Production-ready code
develop       # Development branch

# Feature branches
git checkout -b feature/favorites-system
git checkout -b bugfix/login-redirect
git checkout -b hotfix/stripe-webhook
```

### Commit Messages

**Format**: `<type>(<scope>): <subject>`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```bash
git commit -m "feat(generator): add favorites system"
git commit -m "fix(auth): correct login redirect to /app"
git commit -m "docs(readme): update installation instructions"
git commit -m "refactor(api): extract API client into utility"
```

### Pull Request Process

1. Create feature branch
2. Make changes and commit
3. Push to remote: `git push origin feature/my-feature`
4. Open pull request on GitHub
5. Request code review
6. Address feedback
7. Merge to develop
8. Delete feature branch

---

## Best Practices

### Security
- ✅ Never commit `.env` file (add to `.gitignore`)
- ✅ Use environment variables for all secrets
- ✅ Validate all user input server-side
- ✅ Use HTTPS in production
- ✅ Implement rate limiting on API endpoints
- ✅ Sanitize user-generated content before display

### Performance
- ✅ Use connection pooling for database
- ✅ Cache frequently accessed data
- ✅ Optimize database queries (avoid N+1)
- ✅ Compress responses (gzip)
- ✅ Use CDN for static assets in production
- ✅ Implement pagination for large datasets

### Code Quality
- ✅ Follow PEP 8 for Python code
- ✅ Add type hints to all functions
- ✅ Write docstrings for all public functions
- ✅ Keep functions small and focused (single responsibility)
- ✅ Use meaningful variable names
- ✅ Avoid deep nesting (max 3 levels)
- ✅ Extract magic numbers to constants

### Error Handling
- ✅ Use custom exception classes
- ✅ Log all errors with context
- ✅ Return user-friendly error messages
- ✅ Never expose internal errors to users
- ✅ Implement proper HTTP status codes
- ✅ Handle edge cases explicitly

### Testing
- ✅ Write tests for critical business logic
- ✅ Test happy path and error cases
- ✅ Mock external API calls
- ✅ Aim for >80% code coverage
- ✅ Run tests before committing
- ✅ Use CI/CD to run tests automatically

---

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Supabase Docs**: https://supabase.com/docs
- **Stripe API Docs**: https://stripe.com/docs/api
- **Anthropic Claude Docs**: https://docs.anthropic.com/
- **Udemy Design System**: See `UDEMY_DESIGN_SYSTEM.md`
- **Deployment Guide**: See `DEPLOYMENT_GUIDE.md`
- **Architecture Overview**: See `ARCHITECTURE.md`

---

**Last Updated**: November 30, 2024
**Version**: 1.0
**Questions?**: Open an issue on GitHub or contact the dev team
