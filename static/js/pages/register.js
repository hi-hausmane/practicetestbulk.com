  
    document.getElementById("register-form").addEventListener("submit", async (e) => {
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
