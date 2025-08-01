/**
 * TypeScript-like type definitions for the application
 */

/**
 * @typedef {Object} TireParameters
 * @property {number} Speed
 * @property {number} Throttle  
 * @property {number} Brake
 * @property {number} Surface_Roughness
 * @property {number} front_surface_temp
 * @property {number} rear_surface_temp
 * @property {number} force_on_tire
 */

/**
 * @typedef {Object} TirePredictions
 * @property {number} Tire_wear
 * @property {number} Tire_degreadation
 * @property {number} cumilative_Tire_Wear
 */

/**
 * @typedef {Object} FeatureRange
 * @property {number} min
 * @property {number} max
 * @property {number} mean
 * @property {number} median
 */

/**
 * @typedef {Object} AppState
 * @property {TireParameters} parameters
 * @property {TirePredictions} predictions
 * @property {Object.<string, FeatureRange>} featureRanges
 * @property {boolean} loading
 * @property {string|null} error
 * @property {boolean} initialized
 */

/**
 * @typedef {Object} ApiResponse
 * @property {string} status
 * @property {*} data
 * @property {string} [error]
 */

export const INPUT_VARIABLES = [
  'Speed', 'Throttle', 'Brake', 'Surface_Roughness',
  'front_surface_temp', 'rear_surface_temp', 'force_on_tire'
];

export const OUTPUT_VARIABLES = [
  'Tire_wear', 'Tire degreadation', 'cumilative_Tire_Wear'
];

export const API_ENDPOINTS = {
  INITIALIZE: '/api/initialize',
  PREDICT: '/api/predict',
  HEALTH: '/api/health'
};