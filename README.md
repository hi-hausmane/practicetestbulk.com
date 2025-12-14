# PracticeTestBulk - Practice Test Generator

An AI-powered SaaS platform that generates high-quality Udemy practice test questions using Claude AI. Built with FastAPI, Supabase, and Stripe for a complete production-ready solution.

## ✨ Features

- 🤖 **AI Test Generation** - Create practice tests from course objectives using Claude AI
- 🔐 **Authentication** - Supabase with email/password, Google OAuth, JWT tokens, email verification
- 💳 **Subscription Billing** - Stripe integration with 3 tiers (Free, Pro, Business)
- 📊 **Usage Tracking** - Monthly question limits per tier with real-time tracking
- 📥 **CSV Export** - Generate tests in Udemy bulk import format
- 🎨 **Udemy Design System** - Professional, responsive UI matching Udemy's aesthetic
- 📚 **API Documentation** - Auto-generated OpenAPI/Swagger docs
- ⚡ **Production Ready** - Structured logging, custom exceptions, comprehensive error handling

## 🏗️ Project Structure

```
udemy-practice-test-maker/
├── main.py                     # FastAPI app with OpenAPI docs
├── config.py                   # Centralized configuration & constants
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── auth/                      # Authentication module
│   ├── routes.py             # Auth endpoints (/register, /login, /usage)
│   └── services.py           # Supabase integration
│
├── billing/                   # Billing & subscriptions
│   ├── routes.py             # Stripe endpoints (/subscribe, /webhook)
│   └── services.py           # Stripe checkout & webhook handling
│
├── generator/                 # AI test generation
│   ├── routes.py             # Generation endpoint (/generate)
│   └── services.py           # Claude AI integration & CSV export
│
├── utils/                     # Shared utilities
│   ├── logging_config.py     # Structured logging
│   └── exceptions.py         # Custom exception classes
│
├── static/                    # Frontend assets
│   ├── css/
│   │   └── udemy-theme.css   # Udemy-inspired design system
│   └── js/
│       ├── pages/            # Page-specific JavaScript
│       │   ├── app.js        # Test generator app logic
│       │   ├── pro.js        # Pricing page logic
│       │   ├── landing.js    # Homepage interactivity
│       │   ├── login.js      # Login form handling
│       │   ├── register.js   # Registration handling
│       │   └── verify-email.js
│       └── utils/            # Reusable JS utilities
│           ├── api-client.js # Centralized API client
│           ├── auth.js       # Auth state management
│           └── helpers.js    # UI utility functions
│
├── templates/                 # Jinja2 HTML templates
│   ├── components/           # Reusable components
│   │   ├── nav_landing.html
│   │   ├── nav_app.html
│   │   ├── nav_auth.html
│   │   ├── footer.html
│   │   └── js_utils.html
│   ├── index.html            # Landing page
│   ├── app.html              # Test generator application
│   ├── pro.html              # Pricing & plans
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   └── verify-email.html     # Email verification
│
└── Documentation/
    ├── README.md             # This file
    ├── QUICKSTART.md         # Quick setup guide
    ├── ARCHITECTURE.md       # System architecture
    ├── DEVELOPER_GUIDE.md    # Development guide
    ├── DEPLOYMENT_GUIDE.md   # Deployment instructions
    ├── THEME_README.md       # Design system guide
    └── UDEMY_DESIGN_SYSTEM.md
```

**See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.**

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Supabase account (free tier available)
- Anthropic API key (Claude AI)
- Stripe account (for payment testing)

### 2. Clone & Install

```bash
git clone https://github.com/yourusername/udemy-practice-test-maker.git
cd udemy-practice-test-maker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Go to **Settings → API**
3. Copy these credentials:
   - **Project URL** → `SUPABASE_URL`
   - **anon/public key** → `SUPABASE_ANON_KEY`
   - **service_role key** → `SUPABASE_SERVICE_KEY`

4. **Enable Email Authentication**:
   - Go to **Authentication → Providers**
   - Enable **Email** provider
   - Configure email templates (optional)

5. **Enable Google OAuth** (optional):
   - Go to **Authentication → Providers**
   - Enable **Google** provider
   - Add your Google OAuth credentials

6. Run this SQL in **SQL Editor**:

```sql
-- Add custom fields to auth.users
ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS tier TEXT DEFAULT 'free';
ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS monthly_chars_used INTEGER DEFAULT 0;
ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS username TEXT UNIQUE;

-- Create subscriptions table
CREATE TABLE IF NOT EXISTS subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  tier TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 4. Set Up Anthropic (Claude AI)

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Go to **Account → API Keys**
4. Create a new API key → Copy `ANTHROPIC_API_KEY`

### 5. Set Up Stripe

1. Go to [dashboard.stripe.com](https://dashboard.stripe.com)
2. Toggle to **Test Mode** (for development)
3. Get **Secret Key**:
   - Go to **Developers → API keys**
   - Copy **Secret key** → `STRIPE_SECRET_KEY`
   - Copy **Publishable key** → `STRIPE_PUBLISHABLE_KEY`

4. Create Products:
   - Go to **Products** → **Add product**
   - **Pro Plan**: $9/month (recurring) → Copy Price ID → `STRIPE_PRO_PRICE_ID`
   - **Business Plan**: $19/month (recurring) → Copy Price ID → `STRIPE_BUSINESS_PRICE_ID`

5. Set Up Webhook (for local testing):
   ```bash
   # Install Stripe CLI
   stripe listen --forward-to localhost:8000/webhook

   # Copy the webhook signing secret → STRIPE_WEBHOOK_SECRET
   ```

### 6. Create .env File

Copy `.env.example` to `.env` and fill in your credentials:

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
STRIPE_PRO_PRICE_ID=price_your-pro-price-id
STRIPE_BUSINESS_PRICE_ID=price_your-business-price-id

# Application Settings
APP_ENV=development
LOG_LEVEL=DEBUG
```

### 7. Run the Application

```bash
uvicorn main:app --reload
```

Visit **http://localhost:8000** 🎉

### 8. Access Documentation

- **Landing Page**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

**See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.**

## 💡 How It Works

### 1. User Creates Account
- Sign up with email/password or Google OAuth
- Email verification required
- Starts with Free tier (20 questions/month)

### 2. Generate Practice Tests
- Enter course information:
  - Working title
  - Target audience
  - 4-10 learning objectives
  - Difficulty level (beginner/intermediate/advanced)
  - Course category
- AI generates questions using Claude
- Questions include:
  - Multiple choice format
  - Correct answers
  - Detailed explanations
  - Distractor analysis

### 3. Export to Udemy Format
- Download as CSV file
- Ready for Udemy bulk import
- Includes all required fields:
  - Question text
  - Question type
  - Answer options (1-6)
  - Explanations (1-6)
  - Correct answers
  - Overall explanation
  - Domain/category

### 4. Usage Tracking
- Real-time usage display
- Monthly limits enforced
- Automatic reset each month

## 💰 Subscription Tiers

| Feature | Free | Pro | Business |
|---------|------|-----|----------|
| Questions/Month | 20 | 2,500 | 7,500 |
| Price | $0 | $9/month | $19/month |
| CSV Export | ✅ | ✅ | ✅ |
| Email Support | ❌ | ✅ | ✅ |
| Priority Support | ❌ | ❌ | ✅ |

**Tier configuration**: See `config.py:TIER_LIMITS`

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework with async support
- **Python 3.8+** - Core language
- **Anthropic Claude AI** - AI-powered question generation (claude-3-5-sonnet-20241022)
- **Supabase** - Backend-as-a-Service (Auth + PostgreSQL)
- **Stripe** - Payment processing and subscription management

### Frontend
- **Vanilla JavaScript** - No framework dependencies
- **Jinja2** - Server-side HTML templating
- **Custom CSS** - Udemy-inspired design system
- **Fetch API** - Centralized HTTP client

### Development & Deployment
- **Uvicorn** - ASGI server
- **Git** - Version control
- **Railway/Render** - Deployment platforms (see DEPLOYMENT_GUIDE.md)

## 📡 API Endpoints

### Authentication
- `POST /register` - Create new user account
- `POST /login` - Authenticate user, get JWT token
- `GET /usage` - Get current user tier and usage stats

### Billing
- `POST /subscribe` - Create Stripe checkout session
- `POST /webhook` - Handle Stripe webhook events

### Generator
- `POST /generate` - Generate practice test questions (CSV download)

### Pages (HTML)
- `GET /` - Landing page
- `GET /app` - Test generator application
- `GET /pro` - Pricing & plans
- `GET /login` - Login page
- `GET /register` - Registration page
- `GET /verify-email` - Email verification instructions

### System
- `GET /health` - Health check endpoint
- `GET /api/docs` - Swagger UI (OpenAPI documentation)
- `GET /api/redoc` - ReDoc UI (alternative API docs)

**Example API Usage**:

```bash
# Generate test (requires authentication)
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "num_questions": 10,
    "working_title": "Python Basics",
    "learning_objectives": [
      "Understand variables and data types",
      "Use functions effectively",
      "Work with lists and dictionaries",
      "Handle exceptions properly"
    ],
    "difficulty": "beginner",
    "course_category": "Development"
  }' \
  --output test.csv
```

## 🔐 Environment Variables Reference

| Variable | Description | Where to Get It |
|----------|-------------|-----------------|
| `SUPABASE_URL` | Your Supabase project URL | Supabase Dashboard → Settings → API |
| `SUPABASE_ANON_KEY` | Supabase public/anon key | Supabase Dashboard → Settings → API |
| `SUPABASE_SERVICE_KEY` | Service role key (secret!) | Supabase Dashboard → Settings → API |
| `ANTHROPIC_API_KEY` | Claude AI API key | Anthropic Console → Account → API Keys |
| `STRIPE_SECRET_KEY` | Stripe API secret key | Stripe Dashboard → Developers → API keys |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | Stripe Dashboard → Developers → API keys |
| `STRIPE_PRO_PRICE_ID` | Pro plan price ID ($9/month) | Stripe Dashboard → Products → Pro Plan |
| `STRIPE_BUSINESS_PRICE_ID` | Business plan price ID ($19/month) | Stripe Dashboard → Products → Business Plan |
| `STRIPE_WEBHOOK_SECRET` | Webhook signing secret | Stripe CLI or Dashboard → Webhooks |
| `APP_ENV` | Application environment | `development` or `production` |
| `LOG_LEVEL` | Logging level | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## 📚 Documentation

### Core Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture, data flow, component relationships
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Development setup, code style, adding features
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Production deployment instructions
- **[QUICKSTART.md](QUICKSTART.md)** - Quick setup guide

### Design System
- **[UDEMY_DESIGN_SYSTEM.md](UDEMY_DESIGN_SYSTEM.md)** - Udemy design specifications
- **[THEME_README.md](THEME_README.md)** - Theme usage guide

### API Documentation
Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 🏗️ Development

### Code Organization
```
Module-based architecture:
├── auth/       - Authentication & user management
├── billing/    - Stripe integration & subscriptions
├── generator/  - AI test generation & CSV export
└── utils/      - Shared utilities (logging, exceptions)

Frontend utilities:
└── static/js/
    ├── pages/  - Page-specific logic
    └── utils/  - Reusable helpers (api-client, auth, helpers)
```

### Key Principles
- **Separation of Concerns**: Routes, services, utilities separated
- **DRY**: Shared code in `config.py` and `utils/`
- **Modularity**: Feature-based modules
- **Configuration**: Centralized in `config.py`
- **Logging**: Structured logging throughout

### Adding Features
See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for detailed instructions on:
- Creating new API endpoints
- Adding frontend pages
- Working with the database
- Testing and debugging

## 🚀 Deployment

### Quick Deploy

**Railway** (Recommended):
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Other Platforms**:
- Render
- DigitalOcean App Platform
- Heroku
- Fly.io

**See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment instructions.**

### Production Checklist
- [ ] Set all environment variables
- [ ] Use production Stripe keys
- [ ] Update Stripe webhook endpoint to production URL
- [ ] Enable HTTPS
- [ ] Configure CORS for production domain
- [ ] Set up monitoring and logging
- [ ] Configure email templates in Supabase
- [ ] Test payment flow end-to-end

## 🔒 Security

### Best Practices Implemented
✅ JWT-based authentication
✅ Email verification required
✅ Server-side input validation
✅ Stripe webhook signature verification
✅ Environment variables for secrets
✅ CORS configuration
✅ Structured logging with sensitive data filtering

### Recommended Improvements
- Implement rate limiting (e.g., slowapi)
- Add CSRF tokens for form submissions
- Set Content-Security-Policy headers
- Enable Row Level Security (RLS) in Supabase
- Implement 2FA for high-value accounts
- Regular security audits

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

**See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md#testing) for testing guidelines.**

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Message Format
```
<type>(<scope>): <subject>

Types: feat, fix, docs, style, refactor, test, chore
Example: feat(generator): add favorites system
```

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support & Resources

### Documentation
- **FastAPI**: https://fastapi.tiangolo.com
- **Supabase**: https://supabase.com/docs
- **Stripe**: https://stripe.com/docs
- **Anthropic Claude**: https://docs.anthropic.com

### Getting Help
- Open an issue on GitHub
- Check existing documentation
- Review [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for common tasks

---

## 🎯 Project Status

**Version**: 1.0
**Status**: Production Ready
**Last Updated**: November 30, 2024

### Features Completed
✅ AI-powered test generation with Claude
✅ Full authentication system (email + OAuth)
✅ Stripe subscription billing
✅ Usage tracking and tier enforcement
✅ CSV export in Udemy format
✅ Responsive Udemy-themed UI
✅ Comprehensive documentation
✅ OpenAPI/Swagger documentation

### Roadmap
- [ ] Question favorites/saved tests
- [ ] Bulk generation (multiple courses)
- [ ] Analytics dashboard
- [ ] Team collaboration features
- [ ] API rate limiting
- [ ] Automated testing suite

---

**Built for Udemy course creators to generate high-quality practice tests effortlessly** 🚀
