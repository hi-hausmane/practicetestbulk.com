-- ============================================================================
-- AUTO-CREATE PUBLIC.USERS FOR GOOGLE OAUTH SIGNUPS
-- ============================================================================
-- This trigger automatically creates a record in public.users when a user
-- signs up via Google OAuth (or any OAuth provider)
-- Run this in Supabase SQL Editor
-- ============================================================================

-- Function to handle new user creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
DECLARE
  provider_name TEXT;
  is_oauth BOOLEAN := false;
BEGIN
  -- Check multiple ways to detect OAuth signups
  -- 1. Check app_meta_data.provider (note: it's raw_app_meta_data, not raw_app_metadata)
  provider_name := NEW.raw_app_meta_data->>'provider';

  -- 2. Also check if providers array contains OAuth providers
  IF provider_name IN ('google', 'github', 'gitlab', 'bitbucket', 'azure', 'facebook') THEN
    is_oauth := true;
  ELSIF NEW.raw_app_meta_data->'providers' @> '["google"]'::jsonb THEN
    is_oauth := true;
    provider_name := 'google';
  ELSIF NEW.raw_app_meta_data->'providers' @> '["github"]'::jsonb THEN
    is_oauth := true;
    provider_name := 'github';
  END IF;

  -- If it's an OAuth user, auto-create the public.users record
  IF is_oauth THEN
    INSERT INTO public.users (id, username, email, tier, email_verified, monthly_chars_used)
    VALUES (
      NEW.id,
      COALESCE(NEW.raw_user_meta_data->>'name', NEW.raw_user_meta_data->>'full_name', SPLIT_PART(NEW.email, '@', 1)),
      NEW.email,
      'free',
      true, -- OAuth users are pre-verified by the provider
      0
    )
    ON CONFLICT (id) DO NOTHING;

    RAISE NOTICE 'Auto-created public.users for OAuth user: % (provider: %)', NEW.email, provider_name;
  ELSE
    -- For email/password signups, backend will handle it
    RAISE NOTICE 'Email/password signup detected for: %, skipping auto-create', NEW.email;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Drop existing trigger if it exists
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;

-- Create trigger on auth.users INSERT
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();

-- ============================================================================
-- VERIFICATION & DEBUGGING
-- ============================================================================
-- Test the trigger is installed correctly

SELECT
  trigger_name,
  event_manipulation,
  event_object_table,
  action_statement
FROM information_schema.triggers
WHERE trigger_name = 'on_auth_user_created';

-- ============================================================================
-- DEBUG: Check existing OAuth users
-- ============================================================================
-- Run this to see the metadata structure of your OAuth users
-- This helps debug if the trigger isn't working

SELECT
  id,
  email,
  email_confirmed_at,
  raw_app_metadata->>'provider' as provider,
  raw_app_metadata->'providers' as providers_array,
  raw_user_meta_data->>'name' as google_name,
  raw_user_meta_data->>'full_name' as full_name,
  created_at
FROM auth.users
WHERE email_confirmed_at IS NOT NULL
ORDER BY created_at DESC
LIMIT 5;
