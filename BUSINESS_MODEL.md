# Business Model Documentation

## Overview

TestGenius AI operates as a subscription-based SaaS platform providing AI-powered practice test generation for Udemy course creators. The business model is built on a freemium structure with three tiers.

## Revenue Model

### Subscription Tiers

The platform offers three subscription tiers with increasing capabilities:

#### 1. Free Tier
**Price:** $0/month

**Limits:**
- 20 questions per month
- Maximum 20 questions per test
- Monthly usage resets

**Features:**
- Test the AI quality
- All question formats (single-choice, multiple-select, true/false, scenario-based)
- All explanation styles
- Udemy CSV export
- Email support (48-hour response time)

**Target Audience:**
- New course creators testing the platform
- Occasional users with minimal needs
- Users evaluating quality before purchasing
- Hobbyists creating small courses

**Business Value:**
- Acquisition funnel entry point
- Product quality demonstration
- Word-of-mouth marketing
- Lead generation

---

#### 2. Pro Tier
**Price:** $9/month (monthly) | $90/year ($7.50/month, save 17%)

**Limits:**
- 2,500 questions per month
- Maximum 250 questions per test
- Can create 3-5 complete courses per month (estimated)

**Features:**
- All Free tier features
- Unlimited test downloads
- Higher monthly question quota
- Larger test sizes (up to 250 questions)
- Email support (24-hour response time)

**Target Audience:**
- Professional course creators
- Educators creating multiple courses
- Small content production teams
- Growing Udemy instructors

**Business Value:**
- Primary revenue driver
- Sweet spot for most users
- High conversion potential from Free tier
- Sustainable recurring revenue

**Conversion Strategy:**
- Free users hitting 20-question limit
- Course creators needing larger tests
- Users wanting faster support
- Annual plan discount incentive

---

#### 3. Business Tier
**Price:** $19/month (monthly) | $190/year ($15.83/month, save 17%)

**Limits:**
- 7,500 questions per month
- Maximum 250 questions per test
- Can create 10-15 courses per month (estimated)

**Features:**
- All Pro tier features
- Priority generation (faster processing)
- Perfect for agencies and teams
- Bulk test creation capabilities
- Priority email support (12-hour response time)

**Target Audience:**
- Content agencies
- Corporate training departments
- Course creation teams
- High-volume producers
- Educational institutions

**Business Value:**
- Premium revenue tier
- High-value customers
- Lower churn rate
- Potential for enterprise deals

**Conversion Strategy:**
- Pro users exceeding 2,500 questions
- Agencies managing multiple creators
- Teams needing faster turnaround
- Organizations requiring priority support

---

## Pricing Strategy

### Tier Comparison Matrix

| Feature | Free | Pro | Business |
|---------|------|-----|----------|
| **Monthly Questions** | 20 | 2,500 | 7,500 |
| **Questions per Test** | 20 | 250 | 250 |
| **Estimated Courses/Month** | Test only | 3-5 | 10-15 |
| **CSV Export** | ✅ | ✅ | ✅ |
| **All Question Types** | ✅ | ✅ | ✅ |
| **All Explanation Styles** | ✅ | ✅ | ✅ |
| **Unlimited Downloads** | ❌ | ✅ | ✅ |
| **Email Support** | 48h | 24h | 12h |
| **Priority Generation** | ❌ | ❌ | ✅ |
| **Bulk Creation** | ❌ | ❌ | ✅ |
| **Price (Monthly)** | $0 | $9 | $19 |
| **Price (Annual)** | $0 | $90 ($7.50/mo) | $190 ($15.83/mo) |

### Pricing Rationale

**Free Tier (20 questions):**
- Sufficient to test 1-2 small practice tests
- Low enough to encourage upgrades
- High enough to demonstrate value

**Pro Tier (2,500 questions):**
- Based on typical Udemy course requirements:
  - Average course: 500-800 questions
  - 3-5 courses = 1,500-4,000 questions
- Priced at $9 to be affordable for individual creators
- Annual discount encourages longer commitment

**Business Tier (7,500 questions):**
- Designed for agencies creating 10-15 courses/month
- 2.5x price for 3x capacity (volume discount)
- Priority features justify premium pricing

### Annual Billing Benefits
- **17% discount** on both Pro and Business tiers
- Upfront payment improves cash flow
- Reduces churn (yearly commitment)
- Increases customer lifetime value

---

## Usage Limits & Tracking

### Question Quotas

Quota tracking is based on **questions generated**, not API calls or tests created.

**Example:**
- User generates 1 test with 50 questions = 50 questions used
- User generates 5 tests with 10 questions each = 50 questions used
- Remaining quota: (Monthly limit - Questions used)

### Monthly Reset
- Usage resets on the 1st of each month
- No rollover of unused questions
- Encourages consistent usage

### Enforcement
```python
# From config.py
TIER_LIMITS = {
    "free": {
        "questions_per_month": 20,
        "max_questions_per_test": 20
    },
    "pro": {
        "questions_per_month": 2500,
        "max_questions_per_test": 250
    },
    "business": {
        "questions_per_month": 7500,
        "max_questions_per_test": 250
    }
}
```

**Enforcement Points:**
1. **Pre-generation check** - Verify user has sufficient quota
2. **Post-generation update** - Increment questions_used in database
3. **Real-time display** - Show remaining quota in UI
4. **Limit reached** - Display upgrade prompt

---

## Revenue Projections

### User Funnel Estimates

**Assumptions:**
- 1,000 monthly visitors to landing page
- 10% sign up for Free tier = 100 free users
- 5% of Free users upgrade to Pro = 5 Pro users
- 10% of Pro users upgrade to Business = 0.5 Business users

**Monthly Recurring Revenue (MRR):**
```
Free: 100 users × $0 = $0
Pro: 5 users × $9 = $45
Business: 0.5 users × $19 = $9.50
Total MRR = $54.50
```

**At Scale (10,000 monthly visitors):**
```
Free: 1,000 users × $0 = $0
Pro: 50 users × $9 = $450
Business: 5 users × $19 = $95
Total MRR = $545
```

**Annual Recurring Revenue (ARR):** $545 × 12 = $6,540

### Growth Targets

**Year 1:**
- 1,000 total users
- 50 Pro subscribers ($450 MRR)
- 5 Business subscribers ($95 MRR)
- $545 MRR | $6,540 ARR

**Year 2:**
- 5,000 total users
- 250 Pro subscribers ($2,250 MRR)
- 25 Business subscribers ($475 MRR)
- $2,725 MRR | $32,700 ARR

**Year 3:**
- 15,000 total users
- 750 Pro subscribers ($6,750 MRR)
- 75 Business subscribers ($1,425 MRR)
- $8,175 MRR | $98,100 ARR

---

## Cost Structure

### Variable Costs (Per Question)

**AI API Costs:**

**Claude AI (claude-3-5-sonnet-20241022):**
- Input: $3.00 per 1M tokens
- Output: $15.00 per 1M tokens
- Estimated tokens per question:
  - Input: ~1,000 tokens (prompt)
  - Output: ~500 tokens (question + explanation)
- Cost per question: ~$0.0105

**DeepSeek AI (deepseek-chat):**
- Input: $0.27 per 1M tokens
- Output: $1.10 per 1M tokens
- Same token estimates
- Cost per question: ~$0.00082 (much cheaper)

**Payment Processing (Stripe):**
- 2.9% + $0.30 per transaction
- Pro monthly: $9 × 2.9% + $0.30 = $0.56
- Business monthly: $19 × 2.9% + $0.30 = $0.85

### Fixed Costs (Monthly)

**Infrastructure:**
- Hosting (Railway/Render): $10-50/month
- Supabase (Auth + Database): $0-25/month (depends on scale)
- Domain & SSL: $1-2/month
- Email service (SendGrid/Mailgun): $0-15/month

**Total Fixed Costs:** ~$11-92/month

### Break-Even Analysis

**Using DeepSeek AI (lower cost):**

**Per Pro Subscriber ($9/month):**
- Revenue: $9.00
- AI costs (2,500 questions × $0.00082): $2.05
- Stripe fee: $0.56
- Profit margin: $6.39 (71%)

**Per Business Subscriber ($19/month):**
- Revenue: $19.00
- AI costs (7,500 questions × $0.00082): $6.15
- Stripe fee: $0.85
- Profit margin: $12.00 (63%)

**Break-even point (covering $50/month fixed costs):**
- 8 Pro subscribers = $51.12 profit
- 5 Business subscribers = $60.00 profit
- Or a mix: 6 Pro + 2 Business = $62.34 profit

---

## Customer Lifetime Value (LTV)

### Churn Assumptions

**Free Tier:**
- High churn (50-70% monthly)
- Short engagement
- Main purpose: lead generation

**Pro Tier:**
- Medium churn (5-10% monthly)
- Average lifetime: 12-18 months

**Business Tier:**
- Low churn (2-5% monthly)
- Average lifetime: 24-36 months

### LTV Calculations

**Pro Subscriber:**
- Monthly revenue: $9
- Average lifetime: 15 months
- LTV = $9 × 15 = $135

**Business Subscriber:**
- Monthly revenue: $19
- Average lifetime: 30 months
- LTV = $19 × 30 = $570

### Customer Acquisition Cost (CAC)

**Target CAC:**
- Pro: $45 (CAC:LTV = 1:3 ratio)
- Business: $190 (CAC:LTV = 1:3 ratio)

**Acquisition Channels:**
- Content marketing (blog, tutorials)
- Udemy instructor communities
- Social media (LinkedIn, Twitter)
- Paid ads (Google, Facebook)
- Referral program (future)

---

## Competitive Positioning

### Value Proposition

**vs. Manual Question Writing:**
- 10-20x faster
- AI-powered quality
- Consistent formatting
- Udemy-ready export

**vs. Competitors:**
- Specialized for Udemy format
- Multiple AI models (Claude, DeepSeek)
- Affordable pricing
- No per-question pricing

### Unique Selling Points (USPs)

1. **Udemy-Specific** - Perfect CSV export format
2. **AI-Powered Quality** - Claude or DeepSeek AI
3. **Transparent Pricing** - No hidden fees
4. **Fast Setup** - Start generating in minutes
5. **Flexible Tiers** - Free to Business options

---

## Growth Strategies

### Short-Term (0-6 months)

1. **Free Tier Optimization**
   - Increase free tier sign-ups
   - Improve onboarding experience
   - Add "Upgrade" CTAs at key moments

2. **Content Marketing**
   - Blog posts on Udemy course creation
   - YouTube tutorials
   - Case studies from early users

3. **Community Engagement**
   - Join Udemy instructor forums
   - Facebook groups for course creators
   - Reddit communities (r/Udemy, r/coursedesign)

### Mid-Term (6-12 months)

1. **Feature Expansion**
   - Question bank / favorites
   - Bulk generation (multiple courses)
   - Analytics dashboard
   - Team collaboration

2. **Referral Program**
   - Give 1 month Pro for successful referral
   - Referee gets 20% off first month

3. **Annual Plan Push**
   - Increase annual subscriptions
   - Offer 20% discount (vs. 17%)
   - Better cash flow

### Long-Term (12+ months)

1. **Enterprise Tier**
   - Custom quotas
   - API access
   - White-labeling
   - Dedicated support

2. **Platform Expansion**
   - Support other platforms (Coursera, Skillshare)
   - Multiple export formats
   - More question types

3. **API Monetization**
   - Developer API access
   - Integration partners
   - Zapier/automation tools

---

## Key Performance Indicators (KPIs)

### Acquisition Metrics
- Monthly Active Users (MAU)
- New sign-ups per month
- Sign-up conversion rate (visitor → free user)

### Engagement Metrics
- Tests generated per user
- Questions generated per user
- Monthly active users vs. total users

### Revenue Metrics
- Monthly Recurring Revenue (MRR)
- Annual Recurring Revenue (ARR)
- Average Revenue Per User (ARPU)
- Customer Lifetime Value (LTV)
- Customer Acquisition Cost (CAC)

### Retention Metrics
- Churn rate (monthly)
- Free → Pro conversion rate
- Pro → Business upgrade rate
- Annual plan adoption rate

### Profitability Metrics
- Gross margin per tier
- Break-even point
- CAC:LTV ratio (target 1:3)
- Net revenue retention

---

## Upgrade Triggers

### Free → Pro Conversion

**When to show upgrade prompts:**
1. User reaches 15/20 questions (75% usage)
2. User reaches 20/20 questions (limit hit)
3. User attempts to generate >20 questions in one test
4. After successful test generation (soft prompt)
5. After 3rd test generation in a month

**Messaging:**
- "You're generating great tests! Upgrade to Pro for 2,500 questions/month."
- "Limit reached. Upgrade to Pro to keep creating."
- "Pro users can generate up to 250 questions per test. Upgrade now!"

### Pro → Business Conversion

**When to show upgrade prompts:**
1. User exceeds 2,000 questions (80% usage)
2. User exceeds 2,500 questions (limit hit)
3. User generates >5 tests in a month (high activity)
4. User requests larger test size than 250

**Messaging:**
- "Creating a lot of tests? Business tier offers 7,500 questions/month."
- "Upgrade to Business for priority generation and bulk creation."
- "Agencies love our Business tier. Upgrade for faster support!"

---

## Monetization Optimization

### Annual Plan Incentives

**Current discount:** 17% off (2 months free)

**Possible improvements:**
- Increase to 20% off (2.4 months free)
- Offer annual-only features (e.g., API access)
- Gift annual subscriptions
- Upgrade to annual with prorated credit

### Add-On Services (Future)

**Potential add-ons:**
- Extra question packs ($5 for 500 questions)
- Priority support upgrade ($5/month)
- Custom branding ($10/month)
- API access ($20/month)
- White-label version (enterprise pricing)

### Pricing Experiments

**A/B tests to consider:**
1. $9 vs. $12 for Pro tier
2. Free tier: 10 vs. 20 vs. 30 questions
3. Annual discount: 15% vs. 20% vs. 25%
4. Pay-per-test vs. monthly subscription

---

## Risk Mitigation

### Potential Risks

**1. AI API Cost Increases**
- **Mitigation:** Use DeepSeek (cheaper) or switch providers
- **Action:** Monitor AI costs monthly, adjust tiers if needed

**2. Low Conversion Rates**
- **Mitigation:** Improve onboarding, add features, optimize pricing
- **Action:** Track conversion funnel, run experiments

**3. High Churn**
- **Mitigation:** Improve product value, add engagement features
- **Action:** User interviews, feature requests, retention campaigns

**4. Competitor Entry**
- **Mitigation:** Focus on Udemy specialization, build community
- **Action:** Continuous innovation, customer relationships

**5. Platform Dependency (Udemy format changes)**
- **Mitigation:** Support multiple platforms, stay updated
- **Action:** Monitor Udemy docs, quick adaptation

---

## Success Metrics

### Milestone Goals

**Month 3:**
- 100 total users
- 5 paying customers
- $50 MRR

**Month 6:**
- 500 total users
- 25 paying customers
- $250 MRR

**Month 12:**
- 2,000 total users
- 100 paying customers
- $1,000 MRR

**Month 24:**
- 10,000 total users
- 500 paying customers
- $5,000 MRR

---

## Conclusion

TestGenius AI's freemium SaaS model is designed for sustainable growth with clear upgrade paths, healthy profit margins, and scalable infrastructure. The three-tier system balances accessibility (Free), mainstream adoption (Pro), and premium value (Business), targeting the growing market of Udemy course creators.

**Next Steps:**
- Monitor conversion rates
- Optimize Free → Pro conversion
- Add annual plan incentives
- Expand features for Business tier
- Test pricing experiments

For technical implementation details, see:
- **[CODE_REFERENCE.md](CODE_REFERENCE.md)** - Billing and usage tracking code
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Module organization
