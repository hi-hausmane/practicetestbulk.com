
    // Display the email from URL params or localStorage
    const urlParams = new URLSearchParams(window.location.search);
    const email = urlParams.get('email') || localStorage.getItem('pending_verification_email') || 'your email address';
    document.getElementById('user-email').textContent = email;

    // Store email in localStorage for resend
    if (urlParams.get('email')) {
      localStorage.setItem('pending_verification_email', urlParams.get('email'));
    }

    // Resend verification email function
    async function resendVerificationEmail(event) {
      const email = localStorage.getItem('pending_verification_email');

      if (!email || email === 'your email address') {
        alert('❌ Email not found. Please register again.');
        window.location.href = '/register';
        return;
      }

      const btn = event.target;
      const originalText = btn.textContent;
      btn.textContent = 'Sending...';
      btn.disabled = true;

      try {
        const res = await fetch('/resend-verification', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email })
        });

        if (res.ok) {
          const data = await res.json();
          alert('✅ ' + data.message);
          btn.textContent = '✅ Email Sent!';
          setTimeout(() => {
            btn.textContent = originalText;
            btn.disabled = false;
          }, 3000);
        } else {
          const error = await res.json();
          alert('❌ ' + error.detail);
          btn.textContent = originalText;
          btn.disabled = false;
        }
      } catch (err) {
        alert('❌ Network error: ' + err.message);
        btn.textContent = originalText;
        btn.disabled = false;
      }
    }

    // Make function globally accessible
    window.resendVerificationEmail = resendVerificationEmail;
