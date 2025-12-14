// Check for verification success URL parameter
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('verified') === 'true') {
  document.getElementById('verification-success').style.display = 'block';
}

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
