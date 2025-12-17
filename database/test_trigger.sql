-- ============================================================================
-- TEST OAUTH TRIGGER
-- ============================================================================
-- Run this to see what metadata your OAuth users actually have
-- This will help us understand why the trigger isn't working
-- ============================================================================

-- 1. Check what your actual OAuth user looks like
SELECT
  id,
  email,
  email_confirmed_at,
  raw_app_meta_data,
  raw_user_meta_data,
  created_at
FROM auth.users
WHERE email = 'issarane.hausmane@gmail.com'
ORDER BY created_at DESC
LIMIT 1;

-- 2. Check if user exists in public.users
SELECT
  id,
  username,
  email,
  tier,
  email_verified
FROM public.users
WHERE email = 'issarane.hausmane@gmail.com';

-- 3. Test the trigger function manually with your actual data
-- This simulates what would happen if the trigger fired
DO $$
DECLARE
  test_user RECORD;
  provider_name TEXT;
  is_oauth BOOLEAN := false;
BEGIN
  -- Get your OAuth user data
  SELECT * INTO test_user
  FROM auth.users
  WHERE email = 'issarane.hausmane@gmail.com'
  ORDER BY created_at DESC
  LIMIT 1;

  -- Run the same logic as the trigger
  provider_name := test_user.raw_app_meta_data->>'provider';

  RAISE NOTICE 'Provider from app_meta_data.provider: %', provider_name;
  RAISE NOTICE 'Full app_meta_data: %', test_user.raw_app_meta_data;
  RAISE NOTICE 'Providers array: %', test_user.raw_app_meta_data->'providers';

  IF provider_name IN ('google', 'github', 'gitlab', 'bitbucket', 'azure', 'facebook') THEN
    is_oauth := true;
    RAISE NOTICE 'Detected OAuth via provider field: %', provider_name;
  ELSIF test_user.raw_app_meta_data->'providers' @> '["google"]'::jsonb THEN
    is_oauth := true;
    provider_name := 'google';
    RAISE NOTICE 'Detected OAuth via providers array';
  END IF;

  IF is_oauth THEN
    RAISE NOTICE 'SUCCESS: Would create user for OAuth provider: %', provider_name;
  ELSE
    RAISE NOTICE 'FAILED: Did not detect as OAuth user';
  END IF;
END $$;
