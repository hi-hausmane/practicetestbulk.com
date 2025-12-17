# Google OAuth Setup Guide

## ✅ Step 1: Google Cloud Console (COMPLETED)

You've successfully created OAuth credentials:
- **Client ID**: Stored in `.env` (GOOGLE_CLIENT_ID)
- **Client Secret**: Stored in `.env` (GOOGLE_CLIENT_SECRET)
- **Project**: practicetestbulk

### Configured URIs:
**JavaScript Origins:**
- `https://practicetestbulk.com`
- `https://fxtaavvvsjcwmyvzpook.supabase.co`

**Redirect URIs:**
- `https://practicetestbulk.com/auth/google/callback`
- `https://fxtaavvvsjcwmyvzpook.supabase.co/auth/v1/callback`

---

## 📋 Step 2: Configure Supabase Dashboard (DO THIS NOW)

1. **Go to Supabase Dashboard**: https://supabase.com/dashboard/project/fxtaavvvsjcwmyvzpook

2. **Navigate to Authentication → Providers**

3. **Find "Google" in the provider list and click to configure**

4. **Enable Google Provider** and enter:
   - **Client ID (for OAuth)**: Use the value from `.env` (GOOGLE_CLIENT_ID)
   - **Client Secret (for OAuth)**: Use the value from `.env` (GOOGLE_CLIENT_SECRET)

5. **Save** the configuration

6. **Verify the Callback URL** shown in Supabase matches:
   ```
   https://fxtaavvvsjcwmyvzpook.supabase.co/auth/v1/callback
   ```

---

## 🔧 Step 3: Environment Variables (COMPLETED)

Already added to `.env`:
```bash
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

Check your `.env` file for the actual values (not committed to git for security).

---

## 🚀 Step 4: Add Google Sign-In Button to UI (NEXT)

After Supabase is configured, you'll need to:

1. Add a "Sign in with Google" button to your login and register pages
2. Use Supabase's `signInWithOAuth()` method
3. Handle the OAuth callback redirect

Example code:
```javascript
// Sign in with Google
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'http://localhost:8000/dashboard' // or your preferred redirect
  }
})
```

---

## ⚠️ For Local Development

If you want to test Google OAuth locally, you'll need to add these to Google Cloud Console:

**Additional JavaScript Origins:**
- `http://localhost:8000`

**Additional Redirect URIs:**
- `http://localhost:8000/auth/google/callback`

---

## 🔍 Testing Checklist

- [ ] Configure Google provider in Supabase Dashboard
- [ ] Add "Sign in with Google" button to login page
- [ ] Test Google OAuth flow in production (https://practicetestbulk.com)
- [ ] (Optional) Add localhost URIs and test locally
- [ ] Verify user data is created in `public.users` table after Google sign-in

---

## 📝 Notes

- Google OAuth uses Supabase as the intermediary - users authenticate with Google, then Supabase creates a session
- The `public.users` table should auto-populate when users sign in with Google (handled by existing auth logic in `auth/routes.py:87-136`)
- Email verification is automatic with Google OAuth (users already have verified Google accounts)
