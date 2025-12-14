// Pro.js - Pricing page logic

let currentBilling = 'monthly';

// Toggle between monthly and annual pricing
function toggleBilling(type) {
  currentBilling = type;

  // Update button styles
  const monthlyBtn = document.getElementById('monthlyBtn');
  const annualBtn = document.getElementById('annualBtn');

  if (type === 'monthly') {
    monthlyBtn.style.backgroundColor = 'var(--udemy-white)';
    monthlyBtn.style.boxShadow = 'var(--udemy-shadow-sm)';
    annualBtn.style.backgroundColor = 'transparent';
    annualBtn.style.boxShadow = 'none';

    // Show monthly prices
    document.querySelectorAll('.monthly-price').forEach(el => el.style.display = 'inline');
    document.querySelectorAll('.annual-price').forEach(el => el.style.display = 'none');
  } else {
    annualBtn.style.backgroundColor = 'var(--udemy-white)';
    annualBtn.style.boxShadow = 'var(--udemy-shadow-sm)';
    monthlyBtn.style.backgroundColor = 'transparent';
    monthlyBtn.style.boxShadow = 'none';

    // Show annual prices
    document.querySelectorAll('.monthly-price').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.annual-price').forEach(el => el.style.display = 'inline');
  }
}

// Upgrade to Pro tier
async function upgradeToPro() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    window.location.href = "/login";
    return;
  }

  try {
    const res = await fetch("/create-checkout-session?tier=pro", {
      method: "POST",
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (res.ok) {
      const data = await res.json();
      window.location.href = data.checkout_url;
    } else {
      alert("Error creating checkout session. Please try again.");
    }
  } catch (err) {
    alert("Network error. Please try again.");
  }
}

// Upgrade to Business tier
async function upgradeToBusiness() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    window.location.href = "/login";
    return;
  }

  try {
    const res = await fetch("/create-checkout-session?tier=business", {
      method: "POST",
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (res.ok) {
      const data = await res.json();
      window.location.href = data.checkout_url;
    } else {
      alert("Error creating checkout session. Please try again.");
    }
  } catch (err) {
    alert("Network error. Please try again.");
  }
}
