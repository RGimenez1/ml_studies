/**
 * API Service for communicating with the backend
 */
import axios from 'axios';
import config from '../utils/config';
import { API_ENDPOINTS } from '../types';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: config.API_BASE_URL,
      timeout: config.API_TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error);
        
        if (error.code === 'ECONNREFUSED') {
          throw new Error('Cannot connect to API server. Make sure it\'s running on port 5000.');
        }
        
        if (error.response) {
          throw new Error(error.response.data?.detail || 'API request failed');
        }
        
        throw new Error('Network error occurred');
      }
    );
  }

  /**
   * Initialize the ML models
   * @returns {Promise<Object>} Initialization response with feature ranges
   */
  async initialize() {
    const response = await this.client.get(API_ENDPOINTS.INITIALIZE);
    return response.data;
  }

  /**
   * Make predictions based on input parameters
   * @param {Object} parameters - Input parameters for prediction
   * @returns {Promise<Object>} Prediction results
   */
  async predict(parameters) {
    const response = await this.client.post(API_ENDPOINTS.PREDICT, parameters);
    return response.data;
  }

  /**
   * Check API health status
   * @returns {Promise<Object>} Health status
   */
  async checkHealth() {
    const response = await this.client.get(API_ENDPOINTS.HEALTH);
    return response.data;
  }
}

// Export singleton instance
export default new ApiService();