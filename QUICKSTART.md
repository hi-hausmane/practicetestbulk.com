# 🚀 Quick Start Guide - 5 Minutes to Launch

## Step 1: Install Dependencies (30 seconds)

```bash
pip install -r requirements.txt
```

## Step 2: Get Supabase Credentials (2 minutes)

1. Go to https://supabase.com → New project
2. Settings → API → Copy:
   - `Project URL`
   - `service_role key` (secret!)
   - `JWT Secret`
3. SQL Editor → Run this:

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  username TEXT,
  email TEXT UNIQUE NOT NULL,
  tier TEXT DEFAULT 'free',
  email_verified BOOLEAN DEFAULT false,
  monthly_chars_used INTEGER DEFAULT 0,
  last_reset_date TIMESTAMP DEFAULT NOW(),
  stripe_custom TEXT,
  stripe_subscri TEXT,
  stripe_price_i TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Step 3: Get Stripe Credentials (2 minutes)

1. Go to https://dashboard.stripe.com (Test Mode)
2. Developers → API keys → Copy `Secret key`
3. Products → Create:
   - Pro Plan: $9/month → Copy Price ID
   - Business Plan: $39/month → Copy Price ID
4. Developers → Webhooks → Add:
   - URL: `http://localhost:8000/webhook`
   - Events: `checkout.session.completed`, `customer.subscription.deleted`
   - Copy Signing Secret

## Step 4: Create .env File (30 seconds)

```bash
cp .env.example .env
```

Then fill in your credentials in `.env`

## Step 5: Run! (5 seconds)

```bash
uvicorn main:app --reload
```

Visit http://localhost:8000 🎉

---

## 🛠️ Now Build Your Feature

Copy this prompt into Claude Code:

```
I have a FastAPI SaaS boilerplate with authentication and billing already set up.

I want to build [YOUR APP IDEA].

Please create:
1. A new module for my feature
2. Update app.html with the UI
3. Add usage tracking (free tier limited, pro tier unlimited)
4. Keep existing auth/billing intact
```

**That's it! Auth ✅ Billing ✅ Now just add your unique feature!**
