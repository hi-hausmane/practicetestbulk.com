// Landing.js - Homepage/marketing page logic

// Check authentication status and update buttons
document.addEventListener('DOMContentLoaded', () => {
  // Handle OAuth callback - check if access_token is in URL hash
  if (window.location.hash.includes('access_token')) {
    console.log('[LANDING] OAuth callback detected, extracting token');

    // Extract access_token from URL hash
    const hashParams = new URLSearchParams(window.location.hash.substring(1));
    const accessToken = hashParams.get('access_token');

    if (accessToken) {
      console.log('[LANDING] Storing token and redirecting to /app');
      localStorage.setItem('access_token', accessToken);

      // Redirect to app
      window.location.href = '/app';
      return; // Stop further execution
    }
  }

  const isLoggedIn = Auth.isAuthenticated();

  // Update main CTA button
  const ctaButton = document.getElementById('cta-button');
  if (ctaButton && isLoggedIn) {
    ctaButton.href = '/app';
    ctaButton.textContent = '🚀 Go to App';
  }

  // Update navigation buttons
  const navLogin = document.getElementById('nav-login');
  const navSignup = document.getElementById('nav-signup');
  const navApp = document.getElementById('nav-app');

  if (isLoggedIn) {
    // Hide login/signup, show app button
    if (navLogin) navLogin.style.display = 'none';
    if (navSignup) navSignup.style.display = 'none';
    if (navApp) navApp.style.display = 'inline-flex';
  } else {
    // Show login/signup, hide app button
    if (navLogin) navLogin.style.display = 'inline-block';
    if (navSignup) navSignup.style.display = 'inline-flex';
    if (navApp) navApp.style.display = 'none';
  }
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// Course tab switching
document.querySelectorAll('.course-tab').forEach(tab => {
  tab.addEventListener('click', function() {
    const courseType = this.getAttribute('data-course');

    // Update tab styles
    document.querySelectorAll('.course-tab').forEach(t => {
      t.style.borderBottomColor = 'transparent';
      t.style.color = 'var(--udemy-gray-600)';
      t.classList.remove('active');
    });
    this.style.borderBottomColor = 'var(--udemy-purple)';
    this.style.color = 'var(--udemy-purple)';
    this.classList.add('active');

    // Show corresponding panel
    document.querySelectorAll('.course-panel').forEach(panel => {
      panel.style.display = 'none';
      panel.classList.remove('active');
    });
    const activePanel = document.querySelector(`.course-panel[data-course="${courseType}"]`);
    if (activePanel) {
      activePanel.style.display = 'block';
      activePanel.classList.add('active');
    }
  });
});

// Sub-tab switching (Input/Output)
document.querySelectorAll('.subtab').forEach(subtab => {
  subtab.addEventListener('click', function() {
    const panelId = this.getAttribute('data-panel');
    const parentPanel = this.closest('.course-panel');

    // Update subtab styles within this course panel
    parentPanel.querySelectorAll('.subtab').forEach(st => {
      st.style.backgroundColor = 'var(--udemy-gray-200)';
      st.style.color = 'var(--udemy-gray-700)';
      st.classList.remove('active');
    });
    this.style.backgroundColor = 'var(--udemy-purple)';
    this.style.color = 'white';
    this.classList.add('active');

    // Show corresponding subpanel
    parentPanel.querySelectorAll('.subpanel').forEach(sp => {
      sp.style.display = 'none';
      sp.classList.remove('active');
    });
    const activeSubpanel = document.getElementById(panelId);
    if (activeSubpanel) {
      activeSubpanel.style.display = 'block';
      activeSubpanel.classList.add('active');
    }
  });
});
