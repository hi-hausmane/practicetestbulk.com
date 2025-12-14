/**
 * API Client Utility
 * Centralized API communication with authentication, error handling, and consistent responses
 */

class APIClient {
  constructor() {
    this.baseURL = '';  // Use relative URLs
  }

  /**
   * Get authentication token from localStorage
   */
  getToken() {
    return localStorage.getItem("access_token");
  }

  /**
   * Get default headers with authentication
   */
  getHeaders(customHeaders = {}) {
    const token = this.getToken();
    const headers = {
      "Content-Type": "application/json",
      ...customHeaders
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    return headers;
  }

  /**
   * Handle API response
   */
  async handleResponse(response) {
    // Handle 401 Unauthorized - redirect to login
    if (response.status === 401) {
      localStorage.removeItem("access_token");
      window.location.href = "/login";
      throw new Error("Unauthorized - redirecting to login");
    }

    // Handle other error status codes
    if (!response.ok) {
      let errorMessage = `HTTP Error ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch (e) {
        // Response is not JSON
      }
      throw new Error(errorMessage);
    }

    // Handle different content types
    const contentType = response.headers.get("content-type");

    if (contentType && contentType.includes("application/json")) {
      return await response.json();
    } else if (contentType && (contentType.includes("text/csv") || contentType.includes("application/octet-stream"))) {
      return await response.blob();
    } else {
      return await response.text();
    }
  }

  /**
   * Generic API call
   */
  async call(endpoint, options = {}) {
    const config = {
      ...options,
      headers: this.getHeaders(options.headers || {})
    };

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, config);
      return await this.handleResponse(response);
    } catch (error) {
      console.error(`API Error [${endpoint}]:`, error);
      throw error;
    }
  }

  /**
   * GET request
   */
  async get(endpoint, options = {}) {
    return this.call(endpoint, {
      ...options,
      method: 'GET'
    });
  }

  /**
   * POST request
   */
  async post(endpoint, data = null, options = {}) {
    return this.call(endpoint, {
      ...options,
      method: 'POST',
      body: data ? JSON.stringify(data) : null
    });
  }

  /**
   * PUT request
   */
  async put(endpoint, data = null, options = {}) {
    return this.call(endpoint, {
      ...options,
      method: 'PUT',
      body: data ? JSON.stringify(data) : null
    });
  }

  /**
   * DELETE request
   */
  async delete(endpoint, options = {}) {
    return this.call(endpoint, {
      ...options,
      method: 'DELETE'
    });
  }

  /**
   * Download file (for CSV, etc.)
   */
  async downloadFile(endpoint, filename, data = null) {
    try {
      const blob = await this.post(endpoint, data);

      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      return { success: true, filename };
    } catch (error) {
      console.error('Download error:', error);
      throw error;
    }
  }
}

// Create singleton instance
const api = new APIClient();

// Export for use in other modules
window.api = api;
