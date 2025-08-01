/**
 * Custom hook for managing ML predictions state
 */
import { useState, useEffect, useCallback } from 'react';
import apiService from '../services/apiService';
import { useDebounce } from './useDebounce';
import config from '../utils/config';

export const useMLPredictions = () => {
  const [state, setState] = useState({
    parameters: {},
    predictions: {},
    featureRanges: {},
    loading: true,
    error: null,
    initialized: false,
  });

  // Debounce parameter changes to avoid too many API calls
  const debouncedParameters = useDebounce(state.parameters, config.PREDICTION_DEBOUNCE_MS);

  /**
   * Initialize the application by loading models and feature ranges
   */
  const initialize = useCallback(async () => {
    try {
      setState(prev => ({ ...prev, loading: true, error: null }));
      
      const response = await apiService.initialize();
      
      if (response.status === 'success') {
        // Set initial parameter values to median
        const initialParams = {};
        Object.keys(response.feature_ranges).forEach(key => {
          initialParams[key] = response.feature_ranges[key].median;
        });
        
        setState(prev => ({
          ...prev,
          featureRanges: response.feature_ranges,
          parameters: initialParams,
          initialized: true,
          loading: false,
        }));
        
        // Make initial prediction
        await updatePredictions(initialParams);
      }
    } catch (error) {
      setState(prev => ({
        ...prev,
        error: error.message,
        loading: false,
      }));
    }
  }, []);

  /**
   * Update predictions based on current parameters
   */
  const updatePredictions = useCallback(async (params) => {
    if (!params || Object.keys(params).length === 0) return;
    
    try {
      const response = await apiService.predict(params);
      if (response.status === 'success') {
        setState(prev => ({
          ...prev,
          predictions: response.predictions,
        }));
      }
    } catch (error) {
      console.error('Prediction error:', error);
      // Don't show prediction errors to user, just log them
    }
  }, []);

  /**
   * Update a single parameter value
   */
  const updateParameter = useCallback((parameter, value) => {
    setState(prev => ({
      ...prev,
      parameters: {
        ...prev.parameters,
        [parameter]: value,
      },
    }));
  }, []);

  /**
   * Reset all parameters to their median values
   */
  const resetParameters = useCallback(() => {
    if (Object.keys(state.featureRanges).length === 0) return;
    
    const resetParams = {};
    Object.keys(state.featureRanges).forEach(key => {
      resetParams[key] = state.featureRanges[key].median;
    });
    
    setState(prev => ({
      ...prev,
      parameters: resetParams,
    }));
  }, [state.featureRanges]);

  // Initialize on mount
  useEffect(() => {
    initialize();
  }, [initialize]);

  // Update predictions when parameters change (debounced)
  useEffect(() => {
    if (state.initialized && Object.keys(debouncedParameters).length > 0) {
      updatePredictions(debouncedParameters);
    }
  }, [debouncedParameters, state.initialized, updatePredictions]);

  return {
    ...state,
    updateParameter,
    resetParameters,
    retry: initialize,
  };
};