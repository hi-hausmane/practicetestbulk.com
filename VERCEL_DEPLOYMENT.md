# Vercel Deployment Guide - PracticeTestBulk

## Quick Deploy to Vercel

### Option 1: Deploy via Vercel CLI (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy to Vercel**
   ```bash
   vercel
   ```

   Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N**
   - What's your project's name? **practicetestbulk**
   - In which directory is your code located? **.**

4. **Deploy to Production**
   ```bash
   vercel --prod
   ```

### Option 2: Deploy via Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New Project"
3. Import your Git repository (GitHub/GitLab/Bitbucket)
4. Configure the project:
   - **Framework Preset:** Other
   - **Build Command:** Leave empty
   - **Output Directory:** Leave empty
   - **Install Command:** `pip install -r requirements.txt`

5. Add environment variables (see below)
6. Click "Deploy"

## Required Environment Variables

You **MUST** set these environment variables in your Vercel project settings:

### Authentication (Supabase)
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_JWT_SECRET=your_supabase_jwt_secret
```

### AI Provider (Choose one)

**Option A: DeepSeek (Default)**
```
DEEPSEEK_API_KEY=your_deepseek_api_key
```

**Option B: Anthropic Claude**
```
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### Payment Processing (Stripe)
```
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
```

### Application Settings
```
SECRET_KEY=your_random_secret_key_for_jwt
ENVIRONMENT=production
```

## How to Add Environment Variables in Vercel

### Via Vercel Dashboard:
1. Go to your project in Vercel
2. Click "Settings" → "Environment Variables"
3. Add each variable with its value
4. Select the environment: Production, Preview, Development
5. Click "Save"

### Via Vercel CLI:
```bash
vercel env add SUPABASE_URL
vercel env add SUPABASE_KEY
vercel env add DEEPSEEK_API_KEY
vercel env add STRIPE_SECRET_KEY
# ... add all other variables
```

## Domain Configuration

### Custom Domain Setup:
1. In Vercel Dashboard, go to your project
2. Click "Settings" → "Domains"
3. Add your domain: `practicetestbulk.com`
4. Follow DNS configuration instructions
5. Add these DNS records:
   ```
   Type: A
   Name: @
   Value: 76.76.21.21

   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   ```

## Post-Deployment Configuration

### 1. Update Stripe Webhook URL
After deployment, update your Stripe webhook endpoint:
```
https://practicetestbulk.com/api/billing/webhook
```

### 2. Update Supabase Redirect URLs
Add these URLs to your Supabase project:
- `https://practicetestbulk.com/login`
- `https://practicetestbulk.com/app`

### 3. Update CORS Settings
The app is configured for CORS, but verify your origins in production.

## Vercel Configuration Details

The `vercel.json` file configures:
- **Python Runtime:** Uses `@vercel/python` builder
- **Routes:** Handles static files and FastAPI routing
- **Python Version:** 3.11
- **Region:** US East (iad1) - Change if needed

## Troubleshooting

### Build Failures
- Check build logs in Vercel dashboard
- Verify all dependencies are in `requirements.txt`
- Ensure Python version compatibility (3.11)

### Runtime Errors
- Check Function logs in Vercel dashboard
- Verify environment variables are set correctly
- Check API quotas (Supabase, Stripe, DeepSeek/Claude)

### Static Files Not Loading
- Verify `/static` directory exists
- Check file paths in templates
- Clear Vercel cache: Settings → General → Clear Build Cache

### Database Connection Issues
- Verify Supabase URL and keys
- Check Supabase project is active
- Verify IP allowlist in Supabase (Vercel IPs change)

## Monitoring & Logs

View logs in real-time:
```bash
vercel logs
```

Or in the Vercel dashboard:
- Project → Functions → View Logs

## Redeploy

After making changes:
```bash
git add .
git commit -m "Update application"
git push
```

Vercel will automatically redeploy on push to main branch.

Or manually redeploy:
```bash
vercel --prod
```

## Performance Tips

1. **Enable Caching:** Configure appropriate cache headers for static assets
2. **Optimize Images:** Use WebP format for images in `/static`
3. **Database Indexing:** Ensure proper indexes in Supabase
4. **Rate Limiting:** Monitor API usage for DeepSeek/Claude
5. **CDN:** Vercel automatically uses Edge Network

## Security Checklist

- ✅ All API keys in environment variables (not in code)
- ✅ `.env` file in `.gitignore`
- ✅ HTTPS enabled (automatic with Vercel)
- ✅ Stripe webhook signature verification
- ✅ JWT token validation for auth
- ✅ Rate limiting configured

## Support

- **Vercel Docs:** https://vercel.com/docs
- **FastAPI on Vercel:** https://vercel.com/guides/deploying-fastapi-with-vercel
- **Issues:** Open issue on GitHub repository

---

**Your app will be live at:**
- Default: `https://your-project.vercel.app`
- Custom: `https://practicetestbulk.com`
