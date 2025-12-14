/**
 * Authentication Utilities
 * Helper functions for authentication state management
 */

const Auth = {
  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    return !!localStorage.getItem("access_token");
  },

  /**
   * Get access token
   */
  getToken() {
    return localStorage.getItem("access_token");
  },

  /**
   * Set access token
   */
  setToken(token) {
    localStorage.setItem("access_token", token);
  },

  /**
   * Remove access token (logout)
   */
  removeToken() {
    localStorage.removeItem("access_token");
  },

  /**
   * Logout and redirect
   */
  logout(redirectTo = "/") {
    this.removeToken();
    window.location.href = redirectTo;
  },

  /**
   * Require authentication (redirect if not logged in)
   */
  requireAuth(redirectTo = "/login") {
    if (!this.isAuthenticated()) {
      window.location.href = redirectTo;
      return false;
    }
    return true;
  },

  /**
   * Redirect if already authenticated
   */
  redirectIfAuthenticated(redirectTo = "/app") {
    if (this.isAuthenticated()) {
      window.location.href = redirectTo;
      return true;
    }
    return false;
  }
};

// Export globally
window.Auth = Auth;
