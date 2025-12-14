/**
 * Helper Utilities
 * Common utility functions used across the application
 */

const Helpers = {
  /**
   * Show status/alert message
   */
  showStatus(elementId, message, type = 'info') {
    const statusEl = document.getElementById(elementId);
    if (!statusEl) {
      console.warn(`Status element '${elementId}' not found`);
      return;
    }

    statusEl.textContent = message;

    // Set appropriate class based on type
    const typeClasses = {
      'error': 'udemy-alert udemy-alert-error',
      'success': 'udemy-alert udemy-alert-success',
      'warning': 'udemy-alert udemy-alert-warning',
      'info': 'udemy-alert udemy-alert-info'
    };

    statusEl.className = typeClasses[type] || typeClasses['info'];
    statusEl.style.display = 'block';

    // Auto-hide success and info messages after 5 seconds
    if (type !== 'error' && type !== 'warning') {
      setTimeout(() => {
        statusEl.style.display = 'none';
      }, 5000);
    }
  },

  /**
   * Hide status message
   */
  hideStatus(elementId) {
    const statusEl = document.getElementById(elementId);
    if (statusEl) {
      statusEl.style.display = 'none';
    }
  },

  /**
   * Sanitize filename for download
   */
  sanitizeFilename(filename) {
    return filename.replace(/[^a-z0-9]/gi, '_').toLowerCase();
  },

  /**
   * Format number with commas
   */
  formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  },

  /**
   * Debounce function calls
   */
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  /**
   * Smooth scroll to element
   */
  scrollTo(selector, offset = 0) {
    const element = document.querySelector(selector);
    if (element) {
      const top = element.getBoundingClientRect().top + window.pageYOffset - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  },

  /**
   * Get query parameter from URL
   */
  getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
  },

  /**
   * Copy text to clipboard
   */
  async copyToClipboard(text) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      console.error('Failed to copy to clipboard:', err);
      return false;
    }
  },

  /**
   * Validate email format
   */
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },

  /**
   * Loading button state
   */
  setButtonLoading(button, isLoading, loadingText = 'Loading...') {
    if (!button) return;

    if (isLoading) {
      button.dataset.originalText = button.textContent;
      button.textContent = loadingText;
      button.disabled = true;
    } else {
      button.textContent = button.dataset.originalText || button.textContent;
      button.disabled = false;
      delete button.dataset.originalText;
    }
  }
};

// Export globally
window.Helpers = Helpers;
