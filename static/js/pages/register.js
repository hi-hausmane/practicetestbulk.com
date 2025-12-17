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
  supabase.auth.onAuthStateChange(async (event, session) => {
    if (event === 'SIGNED_IN' && session) {
      // User signed in with Google
      localStorage.setItem("access_token", session.access_token);
      window.location.href = "/app";
    }
  });

  // Handle Google signup button
  const googleBtn = document.getElementById("google-signup-btn");
  if (googleBtn) {
    googleBtn.addEventListener("click", async () => {
      const btn = document.getElementById("google-signup-btn");
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
          alert('Google sign-up failed: ' + error.message);
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
    console.error('Google signup button not found');
  }

  // Handle registration form submission
  const registerForm = document.getElementById("register-form");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const username = document.getElementById("username").value;
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      const submitBtn = e.target.querySelector('button[type="submit"]');
      const originalText = submitBtn.textContent;
      submitBtn.textContent = "Creating account...";
      submitBtn.disabled = true;

      try {
        const res = await fetch("/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, email, password })
        });

        if (res.ok) {
          const data = await res.json();

          // Check if email confirmation is required
          if (data.email_confirmation_required) {
            // Redirect to verification pending page with email in URL
            window.location.href = `/verify-email?email=${encodeURIComponent(email)}`;
          } else if (data.access_token) {
            localStorage.setItem("access_token", data.access_token);
            alert(data.message || "Registration successful!");
            window.location.href = "/app";
          } else {
            alert("Registration successful! Please login.");
            window.location.href = "/login";
          }
        } else {
          const error = await res.json();
          alert("Registration failed: " + error.detail);
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
