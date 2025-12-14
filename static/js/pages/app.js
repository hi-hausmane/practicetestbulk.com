// App.js - Main application logic for the test generator

// Check authentication
const token = localStorage.getItem("access_token");
if (!token) {
  window.location.href = "/login";
}

// Load user data and update UI
async function loadUserData() {
  try {
    const res = await fetch("/usage", {
      headers: { "Authorization": `Bearer ${token}` }
    });

    if (res.ok) {
      const data = await res.json();
      document.getElementById("user-username").textContent = data.username || 'User';
      const tierBadge = document.getElementById("user-tier");
      tierBadge.textContent = data.tier.toUpperCase();

      const upgradeBtn = document.getElementById("upgrade-btn");
      const questionsRemainingEl = document.getElementById("questions-remaining");
      const remainingCountEl = document.getElementById("remaining-count");

      // Show remaining questions for all tiers
      const remaining = data.questions_remaining || 0;
      remainingCountEl.textContent = remaining.toLocaleString();
      questionsRemainingEl.style.display = 'inline';

      // Update color based on remaining questions
      if (data.tier === 'free') {
        const limit = data.monthly_limit || 20;
        const percentage = ((limit - remaining) / limit) * 100;

        if (remaining <= 0) {
          remainingCountEl.style.color = 'var(--udemy-error)';
        } else if (remaining <= 5) {
          remainingCountEl.style.color = 'var(--udemy-warning)';
        } else {
          remainingCountEl.style.color = 'var(--udemy-purple)';
        }
      } else {
        // Pro and Business tiers
        remainingCountEl.style.color = 'var(--udemy-success)';
      }

      if (data.tier === 'business') {
        tierBadge.className = 'udemy-badge udemy-badge-success';
        // Business users - show manage plan
        upgradeBtn.textContent = 'Manage Plan';
        upgradeBtn.style.display = 'inline-block';
        document.getElementById("usage-banner").style.display = 'none';
      } else if (data.tier === 'pro') {
        tierBadge.className = 'udemy-badge udemy-badge-success';
        // Pro users - show manage plan (can upgrade to Business)
        upgradeBtn.textContent = 'Manage Plan';
        upgradeBtn.style.display = 'inline-block';
        document.getElementById("usage-banner").style.display = 'none';
      } else {
        tierBadge.className = 'udemy-badge udemy-badge-purple';
        // Free users - show upgrade
        upgradeBtn.textContent = 'Upgrade ✨';
        upgradeBtn.style.display = 'inline-block';
        document.getElementById("usage-banner").style.display = 'block';

        // Update usage display
        updateUsageDisplay(data);
      }

      // Store user data globally for later use
      window.userData = data;
    } else if (res.status === 401) {
      window.location.href = "/login";
    }
  } catch (err) {
    console.error("Failed to load user data:", err);
  }
}

// Update usage display for free tier users
function updateUsageDisplay(data) {
  const used = data.questions_used || 0;
  const limit = data.monthly_limit || 20;
  const remaining = data.questions_remaining || 0;
  const percentage = Math.round((used / limit) * 100);

  document.getElementById("usage-text").textContent = `${used} of ${limit} questions used (${remaining} remaining)`;
  document.getElementById("usage-percentage").textContent = `${percentage}%`;
  document.getElementById("usage-bar").style.width = `${percentage}%`;

  // Change color based on usage
  const usageBar = document.getElementById("usage-bar");
  const percentageBadge = document.getElementById("usage-percentage");
  const usageBanner = document.getElementById("usage-banner");

  if (percentage >= 90) {
    usageBar.style.backgroundColor = 'var(--udemy-error)';
    percentageBadge.className = 'udemy-badge udemy-badge-error';
    usageBanner.style.borderLeftColor = 'var(--udemy-error)';
  } else if (percentage >= 70) {
    usageBar.style.backgroundColor = 'var(--udemy-warning)';
    percentageBadge.className = 'udemy-badge udemy-badge-warning';
    usageBanner.style.borderLeftColor = 'var(--udemy-warning)';
  } else {
    usageBar.style.backgroundColor = 'var(--udemy-purple)';
    percentageBadge.className = 'udemy-badge udemy-badge-purple';
    usageBanner.style.borderLeftColor = 'var(--udemy-purple)';
  }
}

// Logout function
function logout() {
  localStorage.removeItem("access_token");
  window.location.href = "/";
}

// Learning objectives management
function addObjective() {
  const container = document.getElementById("objectivesContainer");
  const div = document.createElement("div");
  div.style.display = "flex";
  div.style.gap = "8px";
  div.innerHTML = `
    <input
      type="text"
      maxlength="160"
      class="udemy-input objective-input"
      placeholder="Learning objective ${container.children.length + 1}"
      style="flex: 1;"
    />
    <button type="button" onclick="removeObjective(this)" class="udemy-btn udemy-btn-ghost udemy-btn-sm" style="color: var(--udemy-error);">✕</button>
  `;
  container.appendChild(div);
  updateRemoveButtons();
}

function removeObjective(btn) {
  const container = document.getElementById("objectivesContainer");
  if (container.children.length > 4) {
    btn.parentElement.remove();
    updateRemoveButtons();
  }
}

function updateRemoveButtons() {
  const container = document.getElementById("objectivesContainer");
  const removeButtons = container.querySelectorAll('button[type="button"]');
  removeButtons.forEach(btn => {
    btn.style.display = container.children.length > 4 ? 'block' : 'none';
  });
}

// Collect form data
function getFormData() {
  const objectives = Array.from(document.querySelectorAll('.objective-input'))
    .map(input => input.value.trim())
    .filter(val => val.length > 0);

  const formats = Array.from(document.querySelectorAll('input[name="questionFormat"]:checked'))
    .map(cb => cb.value);

  return {
    working_title: document.getElementById('workingTitle').value.trim(),
    practice_test_title: document.getElementById('practiceTestTitle').value.trim(),
    category: document.getElementById('category').value,
    learning_objectives: objectives,
    requirements: document.getElementById('requirements').value.trim() || 'No specific prerequisites',
    target_audience: document.getElementById('targetAudience').value.trim() || 'General learners',
    difficulty_level: document.getElementById('difficultyLevel').value,
    num_questions: parseInt(document.getElementById('numQuestions').value),
    question_formats: formats.length > 0 ? formats : ['single-choice'],
    explanation_style: document.getElementById('explanationStyle').value
  };
}

// Show status message
function showStatus(message, type) {
  const statusEl = document.getElementById('statusMessage');
  statusEl.textContent = message;

  if (type === 'error') {
    statusEl.className = 'udemy-alert udemy-alert-error';
  } else if (type === 'success') {
    statusEl.className = 'udemy-alert udemy-alert-success';
  } else {
    statusEl.className = 'udemy-alert udemy-alert-info';
  }

  statusEl.style.display = 'block';

  if (type !== 'error') {
    setTimeout(() => statusEl.style.display = 'none', 5000);
  }
}

// Check if user has enough questions remaining
function checkUsageLimit(requestedQuestions) {
  if (!window.userData || window.userData.tier !== 'free') {
    return true; // Pro/Business users have no limits
  }

  const used = window.userData.questions_used || 0;
  const limit = window.userData.monthly_limit || 20;
  const remaining = limit - used;

  if (remaining <= 0) {
    showUpgradePrompt('limit-reached', requestedQuestions);
    return false;
  }

  if (requestedQuestions > remaining) {
    showUpgradePrompt('not-enough', requestedQuestions, remaining);
    return false;
  }

  if (remaining <= 5 && remaining > 0) {
    showUpgradePrompt('running-low', requestedQuestions, remaining);
  }

  return true;
}

function showUpgradePrompt(type, requested, remaining = 0) {
  let message = '';

  if (type === 'limit-reached') {
    message = `You've reached your monthly limit of ${window.userData.monthly_limit} questions. Upgrade to Pro for 2,500 questions/month!`;
    showStatus(message, 'error');
    if (confirm(message + '\n\nWould you like to see upgrade options?')) {
      window.location.href = '/pro';
    }
  } else if (type === 'not-enough') {
    message = `You only have ${remaining} questions remaining this month, but you're trying to generate ${requested}. Upgrade to Pro for unlimited generation!`;
    showStatus(message, 'error');
    if (confirm(message + '\n\nWould you like to see upgrade options?')) {
      window.location.href = '/pro';
    }
  } else if (type === 'running-low') {
    message = `⚠️ You only have ${remaining} questions left this month. Consider upgrading to Pro for 2,500 questions/month.`;
    showStatus(message, 'error');
  }
}

// Form submission - Generate and Download CSV
document.getElementById('generatorForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const formData = getFormData();

  if (formData.learning_objectives.length < 4) {
    showStatus('Please provide at least 4 learning objectives', 'error');
    return;
  }

  if (formData.question_formats.length === 0) {
    showStatus('Please select at least one question format', 'error');
    return;
  }

  // Check usage limit before generating
  if (!checkUsageLimit(formData.num_questions)) {
    return;
  }

  const btn = document.getElementById('generateBtn');
  const originalText = btn.textContent;
  btn.disabled = true;
  btn.textContent = 'Generating questions...';
  showStatus('AI is generating your questions. This may take 30-60 seconds...', 'info');

  try {
    const response = await fetch('/api/generator/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(formData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Generation failed');
    }

    // Download the CSV file
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = formData.working_title.replace(/[^a-z0-9]/gi, '_') + '_practice_test.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

    showStatus('CSV file downloaded successfully!', 'success');
    btn.textContent = originalText;
    btn.disabled = false;

    // Reload user data to update usage display
    loadUserData();

  } catch (error) {
    showStatus(`Error: ${error.message}`, 'error');
    btn.textContent = originalText;
    btn.disabled = false;
  }
});

// Update checkbox border on check
document.querySelectorAll('input[name="questionFormat"]').forEach(cb => {
  cb.addEventListener('change', function() {
    const label = this.closest('label');
    if (this.checked) {
      label.style.borderColor = 'var(--udemy-purple)';
      label.style.backgroundColor = 'var(--udemy-purple-lightest)';
    } else {
      label.style.borderColor = 'var(--udemy-gray-400)';
      label.style.backgroundColor = 'transparent';
    }
  });
});

// Initialize
loadUserData();
