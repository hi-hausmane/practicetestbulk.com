# Vercel Environment Variables Setup - Quick Guide

## ⚠️ CRITICAL: You Must Set These Before Your App Will Work

Your app is deployed but **will not work** until you add environment variables in Vercel.

## How to Add Environment Variables in Vercel

### Method 1: Vercel Dashboard (Easiest)

1. Go to your Vercel project dashboard
2. Click **Settings** tab
3. Click **Environment Variables** in the left sidebar
4. Add each variable below (one at a time):
   - **Key**: Enter the variable name (e.g., `SUPABASE_URL`)
   - **Value**: Paste your actual value
   - **Environments**: Select **Production**, **Preview**, and **Development** (all three)
   - Click **Save**

5. After adding ALL variables, go to **Deployments** tab
6. Click the **⋯** menu on your latest deployment
7. Click **Redeploy** → **Redeploy**

### Method 2: Vercel CLI

```bash
# Add each variable
vercel env add SUPABASE_URL production
vercel env add SUPABASE_KEY production
vercel env add SUPABASE_JWT_SECRET production
vercel env add DEEPSEEK_API_KEY production
vercel env add STRIPE_SECRET_KEY production
vercel env add STRIPE_PUBLISHABLE_KEY production
vercel env add STRIPE_WEBHOOK_SECRET production
vercel env add SECRET_KEY production

# Redeploy
vercel --prod
```

## Required Environment Variables

### 1. Supabase Authentication (REQUIRED)

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
SUPABASE_JWT_SECRET=your_supabase_jwt_secret_here
```

**Where to find these:**
- Go to your Supabase project dashboard
- Click **Settings** → **API**
- **Project URL** = `SUPABASE_URL`
- **anon public** key = `SUPABASE_KEY`
- **JWT Secret** = `SUPABASE_JWT_SECRET`

### 2. AI Provider (Choose ONE)

**Option A: DeepSeek (Cheaper, Default)**
```
DEEPSEEK_API_KEY=sk-your_deepseek_api_key
```
Get key from: https://platform.deepseek.com

**Option B: Anthropic Claude**
```
ANTHROPIC_API_KEY=sk-ant-your_anthropic_key
```
Get key from: https://console.anthropic.com

### 3. Stripe Payment Processing (REQUIRED)

```
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

**Where to find these:**
- Go to https://dashboard.stripe.com
- Click **Developers** → **API keys**
- Copy **Secret key** and **Publishable key**
- For webhook secret:
  1. Go to **Developers** → **Webhooks**
  2. Click **Add endpoint**
  3. URL: `https://your-app.vercel.app/api/billing/webhook`
  4. Events: Select `checkout.session.completed` and `customer.subscription.updated`
  5. After creating, copy the **Signing secret**

### 4. Application Secret (REQUIRED)

```
SECRET_KEY=your_random_secret_key_minimum_32_chars
```

**Generate a random secret:**
```bash
# On Mac/Linux
openssl rand -hex 32

# Or use Python
python -c "import secrets; print(secrets.token_hex(32))"
```

## Verification Checklist

After setting all environment variables:

- [ ] SUPABASE_URL is set
- [ ] SUPABASE_KEY is set
- [ ] SUPABASE_JWT_SECRET is set
- [ ] DEEPSEEK_API_KEY **or** ANTHROPIC_API_KEY is set
- [ ] STRIPE_SECRET_KEY is set
- [ ] STRIPE_PUBLISHABLE_KEY is set
- [ ] STRIPE_WEBHOOK_SECRET is set
- [ ] SECRET_KEY is set (32+ characters)
- [ ] Redeployed after adding variables
- [ ] App loads without 500 error

## Testing Your Deployment

Once environment variables are set and redeployed:

1. Visit your app URL: `https://your-app.vercel.app`
2. The homepage should load ✅
3. Try accessing `/health` endpoint: Should return `{"status": "healthy"}`
4. Check function logs: Settings → Functions → View Logs

## Common Issues

### ❌ "Authentication service not configured"
**Fix:** Add SUPABASE_URL and SUPABASE_KEY, then redeploy

### ❌ "RuntimeError: SUPABASE_URL must be set"
**Fix:** You're on an old deployment. Add env vars and **redeploy**

### ❌ Stripe errors
**Fix:** Add all three Stripe keys (secret, publishable, webhook)

### ❌ AI generation fails
**Fix:** Add DEEPSEEK_API_KEY or ANTHROPIC_API_KEY

## Quick Copy-Paste Template

Copy your `.env` file values and paste them one by one in Vercel:

```bash
# From your local .env file
cat .env
```

## Need Help?

- **Vercel Docs:** https://vercel.com/docs/concepts/projects/environment-variables
- **Supabase Docs:** https://supabase.com/docs/guides/api
- **Stripe Docs:** https://stripe.com/docs/keys

---

**After setting all variables, your app will work! 🎉**
