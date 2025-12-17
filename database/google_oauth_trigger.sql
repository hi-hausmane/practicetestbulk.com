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
BEGIN
  -- Insert into public.users when a new user is created in auth.users
  INSERT INTO public.users (id, username, email, tier, email_verified, monthly_chars_used)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'name', SPLIT_PART(NEW.email, '@', 1)), -- Use Google name or email prefix
    NEW.email,
    'free',
    NEW.email_confirmed_at IS NOT NULL, -- OAuth users are pre-verified
    0
  )
  ON CONFLICT (id) DO NOTHING; -- Prevent duplicate insertion

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
-- VERIFICATION
-- ============================================================================
-- Test the trigger is installed correctly

SELECT
  trigger_name,
  event_manipulation,
  event_object_table,
  action_statement
FROM information_schema.triggers
WHERE trigger_name = 'on_auth_user_created';
