/**
 * Application configuration
 */

const config = {
  API_BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000',
  API_TIMEOUT: parseInt(process.env.REACT_APP_API_TIMEOUT) || 10000,
  
  // UI Configuration
  THEME: {
    PRIMARY: '#1976d2',
    SECONDARY: '#dc004e',
    BACKGROUND: '#f5f5f5',
    SUCCESS: '#4caf50',
    WARNING: '#ff9800',
    ERROR: '#f44336',
  },
  
  // Application behavior
  PREDICTION_DEBOUNCE_MS: 300,
  SLIDER_STEPS: 100,
  VALUE_PRECISION: 3,
};

export default config;