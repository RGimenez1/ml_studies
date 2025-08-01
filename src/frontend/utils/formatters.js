/**
 * Brazilian formatting utilities with proper units and localization
 */
import config from './config';

/**
 * Format a number using Brazilian locale (comma for decimals, dot for thousands)
 * @param {number} value - The value to format
 * @param {number} precision - Number of decimal places
 * @returns {string} Formatted value in Brazilian format
 */
export const formatBrazilianNumber = (value, precision = 2) => {
  if (typeof value !== 'number' || isNaN(value)) return '0,00';
  
  return value.toLocaleString('pt-BR', {
    minimumFractionDigits: precision,
    maximumFractionDigits: precision
  });
};

/**
 * Format a value with appropriate unit and Brazilian formatting
 * @param {number} value - The value to format
 * @param {string} parameter - Parameter name to determine unit
 * @returns {string} Formatted value with unit
 */
export const formatValueWithUnit = (value, parameter) => {
  if (typeof value !== 'number' || isNaN(value)) return '0,00';

  const units = {
    'Speed': 'km/h',
    'Throttle': '%', 
    'Brake': '%',
    'Surface_Roughness': '',
    'front_surface_temp': '°C',
    'rear_surface_temp': '°C', 
    'force_on_tire': 'kN',
    'Tire_wear': '%',
    'Tire degreadation': '%',
    'cumilative_Tire_Wear': '%'
  };

  const conversions = {
    'Throttle': v => v * 100,
    'Brake': v => v * 100,
    'force_on_tire': v => v / 1000, // Convert N to kN
    'Tire_wear': v => v * 100,
    'cumilative_Tire_Wear': v => v * 100
  };

  const unit = units[parameter] || '';
  const convertedValue = conversions[parameter] ? conversions[parameter](value) : value;
  
  let precision = 1;
  if (parameter === 'Surface_Roughness') precision = 2;
  if (parameter === 'force_on_tire') precision = 1;
  if (['Throttle', 'Brake', 'Tire_wear', 'cumilative_Tire_Wear'].includes(parameter)) precision = 1;

  const formattedValue = formatBrazilianNumber(convertedValue, precision);
  return unit ? `${formattedValue} ${unit}` : formattedValue;
};

/**
 * Get Brazilian parameter names for display
 * @param {string} paramName - Parameter name
 * @returns {string} Brazilian Portuguese parameter name
 */
export const formatParameterName = (paramName) => {
  const brazilianNames = {
    'Speed': 'Velocidade',
    'Throttle': 'Aceleração',
    'Brake': 'Freio',
    'Surface_Roughness': 'Rugosidade da Pista',
    'front_surface_temp': 'Temperatura Frontal',
    'rear_surface_temp': 'Temperatura Traseira',
    'force_on_tire': 'Força no Pneu',
    'Tire_wear': 'Desgaste do Pneu',
    'Tire degreadation': 'Degradação do Pneu',
    'cumilative_Tire_Wear': 'Desgaste Acumulado'
  };

  return brazilianNames[paramName] || paramName.replace(/_/g, ' ');
};

/**
 * Legacy function for backward compatibility
 * @param {number} value - The value to format
 * @param {number} precision - Number of decimal places (default from config)
 * @returns {string} Formatted value
 */
export const formatValue = (value, precision = config.VALUE_PRECISION) => {
  return formatBrazilianNumber(value, precision);
};

/**
 * Get color based on parameter value relative to its range
 * @param {string} parameter - Parameter name
 * @param {number} value - Current value
 * @param {Object} featureRanges - Feature ranges object
 * @returns {string} MUI color name
 */
export const getValueColor = (parameter, value, featureRanges) => {
  if (!featureRanges[parameter]) return 'primary';
  
  const range = featureRanges[parameter];
  const normalized = (value - range.min) / (range.max - range.min);
  
  if (normalized < 0.3) return 'success';
  if (normalized > 0.7) return 'error';
  return 'warning';
};

/**
 * Get slider step size based on range
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {number} Step size
 */
export const getSliderStep = (min, max) => {
  return (max - min) / config.SLIDER_STEPS;
};

/**
 * Check if a value is considered high compared to the mean
 * @param {number} value - Value to check
 * @param {number} mean - Mean value for comparison
 * @returns {boolean} True if value is high
 */
export const isValueHigh = (value, mean) => {
  return value > (mean || 0);
};

/**
 * Get insight label based on value and thresholds
 * @param {number} value - Current value
 * @param {Object} range - Feature range object
 * @returns {string} Insight label
 */
export const getInsightLabel = (value, range) => {
  if (!range) return 'Desconhecido';
  
  const normalized = (value - range.min) / (range.max - range.min);
  
  if (normalized < 0.3) return 'Baixo';
  if (normalized > 0.7) return 'Alto';
  return 'Médio';
};