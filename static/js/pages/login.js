// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize Supabase client
  const SUPABASE_URL = 'https://fxtaavvvsjcwmyvzpook.supabase.co';
  const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ4dGFhdnZ2c2pjd215dnpwb29rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ0MTI0MDYsImV4cCI6MjA3OTk4ODQwNn0.-D4xhMPONSax-XGeYVpxgH3JsEorNIRzNwNlWdOYm8I';

  if (!window.supabase) {
    console.error('Supabase library not loaded');
    return;
  }

  const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

  // Check for OAuth callback with session
  // Only handle SIGNED_IN event after OAuth redirect (not on page load)
  supabase.auth.onAuthStateChange(async (event, session) => {
    if (event === 'SIGNED_IN' && session) {
      // Check if this is from OAuth callback (URL will have access_token hash)
      if (window.location.hash.includes('access_token')) {
        console.log('[AUTH] OAuth callback detected, redirecting to /app');
        localStorage.setItem("access_token", session.access_token);
        window.location.href = "/app";
      }
    }
  });

  // Check for verification success URL parameter
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('verified') === 'true') {
    const successEl = document.getElementById('verification-success');
    if (successEl) {
      successEl.style.display = 'block';
    }
  }

  // Handle Google login button
  const googleBtn = document.getElementById("google-login-btn");
  if (googleBtn) {
    googleBtn.addEventListener("click", async () => {
      const btn = document.getElementById("google-login-btn");
      const originalHTML = btn.innerHTML;
      btn.innerHTML = '<span>Connecting to Google...</span>';
      btn.disabled = true;

      try {
        const { data, error } = await supabase.auth.signInWithOAuth({
          provider: 'google',
          options: {
            redirectTo: `${window.location.origin}/app`
          }
        });

        if (error) {
          alert('Google sign-in failed: ' + error.message);
          btn.innerHTML = originalHTML;
          btn.disabled = false;
        }
        // If successful, user will be redirected to Google login
      } catch (err) {
        alert('Error: ' + err.message);
        btn.innerHTML = originalHTML;
        btn.disabled = false;
      }
    });
  } else {
    console.error('Google login button not found');
  }

  // Handle login form submission
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      const submitBtn = e.target.querySelector('button[type="submit"]');
      const originalText = submitBtn.textContent;
      submitBtn.textContent = "Signing in...";
      submitBtn.disabled = true;

      try {
        const res = await fetch("/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password })
        });

        if (res.ok) {
          const data = await res.json();

          // Store access token in localStorage
          if (data.access_token) {
            localStorage.setItem("access_token", data.access_token);

            // Redirect to /app
            window.location.href = "/app";
          } else {
            alert("Login successful but no token received. Please try again.");
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
          }
        } else {
          const error = await res.json();
          alert("Login failed: " + (error.detail || "Invalid credentials"));
          submitBtn.textContent = originalText;
          submitBtn.disabled = false;
        }
      } catch (err) {
        alert("Network error: " + err.message);
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
      }
    });
  }
});
