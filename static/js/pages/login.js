// Initialize Supabase client
const SUPABASE_URL = 'https://fxtaavvvsjcwmyvzpook.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ4dGFhdnZ2c2pjd215dnpwb29rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ0MTI0MDYsImV4cCI6MjA3OTk4ODQwNn0.-D4xhMPONSax-XGeYVpxgH3JsEorNIRzNwNlWdOYm8I';

const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Check for OAuth callback with session
supabase.auth.onAuthStateChange(async (event, session) => {
  if (event === 'SIGNED_IN' && session) {
    // User signed in with Google
    localStorage.setItem("access_token", session.access_token);
    window.location.href = "/app";
  }
});

// Check for verification success URL parameter
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('verified') === 'true') {
  document.getElementById('verification-success').style.display = 'block';
}

// Handle Google login button
document.getElementById("google-login-btn").addEventListener("click", async () => {
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

// Handle login form submission
document.getElementById("login-form").addEventListener("submit", async (e) => {
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
