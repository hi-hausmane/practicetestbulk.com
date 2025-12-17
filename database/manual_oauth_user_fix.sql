-- ============================================================================
-- MANUAL FIX: Create missing public.users for existing OAuth users
-- ============================================================================
-- Use this to manually create public.users records for OAuth users
-- that signed up before the trigger was installed
-- ============================================================================

-- Step 1: Check which OAuth users are missing from public.users
SELECT
  au.id,
  au.email,
  au.raw_app_metadata->>'provider' as provider,
  au.raw_app_metadata->'providers' as providers_array,
  au.raw_user_meta_data->>'name' as google_name,
  CASE WHEN pu.id IS NULL THEN 'MISSING' ELSE 'EXISTS' END as status
FROM auth.users au
LEFT JOIN public.users pu ON au.id = pu.id
WHERE au.email_confirmed_at IS NOT NULL
ORDER BY au.created_at DESC;

-- Step 2: Manually insert missing OAuth users into public.users
-- This will create records for any OAuth user that's missing
INSERT INTO public.users (id, username, email, tier, email_verified, monthly_chars_used)
SELECT
  au.id,
  COALESCE(
    au.raw_user_meta_data->>'name',
    au.raw_user_meta_data->>'full_name',
    SPLIT_PART(au.email, '@', 1)
  ) as username,
  au.email,
  'free' as tier,
  true as email_verified,
  0 as monthly_chars_used
FROM auth.users au
LEFT JOIN public.users pu ON au.id = pu.id
WHERE au.email_confirmed_at IS NOT NULL
  AND pu.id IS NULL  -- Only insert if not already in public.users
  AND (
    au.raw_app_metadata->>'provider' IN ('google', 'github', 'gitlab', 'bitbucket', 'azure', 'facebook')
    OR au.raw_app_metadata->'providers' @> '["google"]'::jsonb
    OR au.raw_app_metadata->'providers' @> '["github"]'::jsonb
  )
ON CONFLICT (id) DO NOTHING;

-- Step 3: Verify all users are now in public.users
SELECT
  COUNT(*) as oauth_users_in_auth,
  (SELECT COUNT(*) FROM public.users WHERE email_verified = true) as oauth_users_in_public,
  COUNT(*) - (SELECT COUNT(*) FROM public.users WHERE email_verified = true) as missing_users
FROM auth.users
WHERE email_confirmed_at IS NOT NULL;
