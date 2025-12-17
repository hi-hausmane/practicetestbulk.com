# Google OAuth Issues and Fixes

## Issue 1: Users Not Created in public.users After Google OAuth ❌

### Problem:
When users sign up via Google OAuth, they are created in `auth.users` (Supabase authentication table) but NOT in `public.users` (our application table). This causes errors when trying to access user data.

### Root Cause:
No database trigger exists to auto-create `public.users` records when OAuth users sign up.

### Solution:
Run the SQL script to create an auto-trigger:

**File:** `database/google_oauth_trigger.sql`

**Steps:**
1. Go to Supabase Dashboard → SQL Editor: https://supabase.com/dashboard/project/fxtaavvvsjcwmyvzpook/sql/new
2. Copy and paste the contents of `database/google_oauth_trigger.sql`
3. Click "Run"

**What it does:**
- Creates a trigger `on_auth_user_created` on the `auth.users` table
- **Only triggers for OAuth signups** (Google, GitHub, etc.) - not for regular email/password signups
- Regular email/password signups are handled by the backend code in `auth/routes.py`
- Sets default values: tier=free, email_verified=true (OAuth users are pre-verified)
- Uses Google name from metadata or email prefix as username
- Uses `ON CONFLICT DO NOTHING` to prevent duplicate insertion errors

---

## Issue 2: Login Button Not Working After First Click ⚠️

### Problem:
On the **login page**, after clicking "Continue with Google" once, the button may not work on subsequent attempts (within the same session).

### Possible Causes:
1. **Auth state listener conflict**: The `onAuthStateChange` listener might be interfering
2. **Button stays disabled**: If there's an error, the button might not re-enable properly
3. **Multiple event listeners**: DOMContentLoaded might attach multiple listeners if called twice

### Current Code Behavior:
- Register button: Works ✅
- Login button: May fail after first attempt ❌

### Investigation Needed:
Check browser console for errors when clicking the login button:
- "Supabase library not loaded"
- "Google login button not found"
- Any Supabase API errors

### Temporary Workaround:
Refresh the page and try again (not ideal)

---

## Issue 3: Supabase Redirect URLs Configuration

### Correct Configuration:

**Supabase Dashboard → Authentication → URL Configuration:**
- **Site URL**: `https://practicetestbulk.com`
- **Redirect URLs**:
  - `https://practicetestbulk.com/**`
  - `https://practicetestbulk.com/app`
  - `http://localhost:8000/**` (for local development)

**Google Cloud Console → OAuth Credentials:**
- **Authorized JavaScript origins**:
  - `https://practicetestbulk.com`
  - `https://fxtaavvvsjcwmyvzpook.supabase.co`
  - `http://localhost:8000` (optional, for local testing)

- **Authorized redirect URIs**:
  - `https://practicetestbulk.com/auth/google/callback`
  - `https://fxtaavvvsjcwmyvzpook.supabase.co/auth/v1/callback`
  - `http://localhost:8000/auth/google/callback` (optional)

---

## Testing Checklist

### After running the SQL trigger:
- [ ] Sign up with Google OAuth on `/register`
- [ ] Verify user appears in Supabase: `SELECT * FROM public.users ORDER BY created_at DESC;`
- [ ] Check that `email_verified` is `true`
- [ ] Check that `tier` is `free`
- [ ] Check that username is populated (from Google name or email)

### Login button testing:
- [ ] Click "Continue with Google" on `/login` - should redirect ✅
- [ ] Complete Google authentication
- [ ] Should redirect back to `/app`
- [ ] Try logging out and logging in again - button should still work

---

## Next Steps

1. **Run the SQL trigger** in Supabase (most important!)
2. **Debug the login button** issue - check browser console
3. **Test full OAuth flow** from register → login → app access
4. **Monitor logs** for any authentication errors

