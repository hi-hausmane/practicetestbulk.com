# Question Quota Display Feature

## Summary
Added a prominent display of remaining questions for all user tiers (Free, Pro, Business) in the navigation bar and enhanced the usage banner for free tier users.

---

## Changes Made

### 1. **Navigation Bar Enhancement** (templates/app.html:28-30)

Added a new badge next to the user tier showing remaining questions:

```html
<span id="questions-remaining" class="udemy-body-sm" style="font-weight: 500; color: var(--udemy-gray-700); display: none;">
  <span style="color: var(--udemy-purple); font-weight: 600;" id="remaining-count">0</span> questions left
</span>
```

**Visual Example:**
```
┌────────────────────────────────────────────────────────┐
│ TestGenius AI                    User  [PRO]  2,450 questions left  │
│                                        Manage Plan    Logout         │
└────────────────────────────────────────────────────────┘
```

---

### 2. **JavaScript Logic Updates** (static/js/pages/app.js)

#### Added Remaining Questions Display (lines 23-46):
```javascript
const questionsRemainingEl = document.getElementById("questions-remaining");
const remainingCountEl = document.getElementById("remaining-count");

// Show remaining questions for all tiers
const remaining = data.questions_remaining || 0;
remainingCountEl.textContent = remaining.toLocaleString();
questionsRemainingEl.style.display = 'inline';

// Update color based on remaining questions
if (data.tier === 'free') {
  if (remaining <= 0) {
    remainingCountEl.style.color = 'var(--udemy-error)';      // Red
  } else if (remaining <= 5) {
    remainingCountEl.style.color = 'var(--udemy-warning)';    // Orange
  } else {
    remainingCountEl.style.color = 'var(--udemy-purple)';     // Purple
  }
} else {
  // Pro and Business tiers
  remainingCountEl.style.color = 'var(--udemy-success)';     // Green
}
```

#### Enhanced Usage Banner Text (line 88):
```javascript
document.getElementById("usage-text").textContent =
  `${used} of ${limit} questions used (${remaining} remaining)`;
```

---

## Feature Behavior by Tier

### **Free Tier (20 questions/month)**
- Shows remaining count in navigation: `15 questions left`
- Color changes based on usage:
  - **Green/Purple**: >5 questions remaining
  - **Orange**: 1-5 questions remaining
  - **Red**: 0 questions remaining
- Usage banner displays: `15 of 20 questions used (5 remaining)`
- Progress bar shows percentage used

### **Pro Tier (2,500 questions/month)**
- Shows remaining count in navigation: `2,450 questions left`
- Color: **Green** (success color)
- No usage banner (cleaner interface)
- Comma-separated for readability (e.g., `2,450`)

### **Business Tier (7,500 questions/month)**
- Shows remaining count in navigation: `7,250 questions left`
- Color: **Green** (success color)
- No usage banner (cleaner interface)
- Comma-separated for readability (e.g., `7,250`)

---

## Backend Support

The backend already supports this feature via the `/usage` endpoint (auth/routes.py:221-240):

```python
@auth_router.get("/usage")
async def get_usage(current_user: dict = Depends(get_current_user)):
    tier = current_user.get("tier", "free")
    monthly_limit = get_monthly_question_limit(tier)
    questions_used = current_user.get("monthly_chars_used", 0)

    return {
        "username": current_user.get("username"),
        "tier": tier,
        "monthly_limit": monthly_limit,
        "questions_used": questions_used,
        "questions_remaining": max(0, monthly_limit - questions_used),  # ← Key field
        "email_verified": current_user.get("email_verified", False)
    }
```

---

## Visual Design Examples

### Free Tier (Low Usage)
```
┌──────────────────────────────────────────────────────────────┐
│ User  [FREE]  18 questions left  Upgrade ✨  Logout          │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Your Usage This Month                              [10%]      │
│ ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░        │
│ 2 of 20 questions used (18 remaining)                         │
│                                       [Upgrade to Pro]         │
└──────────────────────────────────────────────────────────────┘
```

### Free Tier (High Usage - Warning)
```
┌──────────────────────────────────────────────────────────────┐
│ User  [FREE]  3 questions left  Upgrade ✨  Logout            │
│              ⚠️ (orange)                                       │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ Your Usage This Month                              [85%]      │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░          │
│ 17 of 20 questions used (3 remaining)                         │
│                                       [Upgrade to Pro]         │
└──────────────────────────────────────────────────────────────┘
```

### Pro Tier
```
┌──────────────────────────────────────────────────────────────┐
│ User  [PRO]  2,450 questions left  Manage Plan  Logout        │
│              ✓ (green)                                         │
└──────────────────────────────────────────────────────────────┘

(No usage banner - cleaner interface)
```

### Business Tier
```
┌──────────────────────────────────────────────────────────────┐
│ User  [BUSINESS]  7,250 questions left  Manage Plan  Logout   │
│                   ✓ (green)                                    │
└──────────────────────────────────────────────────────────────┘

(No usage banner - cleaner interface)
```

---

## User Experience Improvements

1. **Always Visible**: Question quota is now visible in the nav bar on every page
2. **Color-Coded**: Visual feedback based on remaining quota
3. **Number Formatting**: Large numbers use commas (e.g., 2,450)
4. **Real-time Updates**: Counter updates after question generation
5. **Tier-Appropriate**: Different styling for each tier level

---

## Testing

To test the feature:

1. Start the development server:
   ```bash
   cd "/home/h/Documents/GitHub/Udemy Practice Test Maker"
   uvicorn main:app --reload
   ```

2. Log in with different tier accounts and verify:
   - Free tier shows quota with color changes
   - Pro tier shows green quota number
   - Business tier shows green quota number
   - Usage banner only appears for free tier

3. Generate questions and verify the counter updates

---

## Files Modified

1. `templates/app.html` - Added remaining questions badge to navigation
2. `static/js/pages/app.js` - Added logic to display and update remaining questions
3. `auth/routes.py` - Already had backend support (no changes needed)

---

## Future Enhancements

Potential improvements:
- Add animation when quota changes
- Add tooltip showing monthly reset date
- Show usage trend (up/down from last month)
- Add warning notification when approaching limit
