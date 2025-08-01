import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Slider,
  Box,
  Paper,
  CircularProgress,
  Alert,
  Chip
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  const [parameters, setParameters] = useState({});
  const [predictions, setPredictions] = useState({});
  const [featureRanges, setFeatureRanges] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize the app
  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      setLoading(true);
      const response = await axios.get('http://localhost:5000/api/initialize');
      
      if (response.data.status === 'success') {
        setFeatureRanges(response.data.feature_ranges);
        
        // Set initial parameter values to median
        const initialParams = {};
        Object.keys(response.data.feature_ranges).forEach(key => {
          initialParams[key] = response.data.feature_ranges[key].median;
        });
        
        setParameters(initialParams);
        updatePredictions(initialParams);
      }
    } catch (err) {
      setError('Failed to initialize. Make sure Python API server is running on port 5000.');
      console.error('Initialization error:', err);
    } finally {
      setLoading(false);
    }
  };

  const updatePredictions = async (params) => {
    try {
      const response = await axios.post('http://localhost:5000/api/predict', params);
      if (response.data.status === 'success') {
        setPredictions(response.data.predictions);
      }
    } catch (err) {
      console.error('Prediction error:', err);
    }
  };

  const handleParameterChange = (parameter, newValue) => {
    const updatedParams = { ...parameters, [parameter]: newValue };
    setParameters(updatedParams);
    updatePredictions(updatedParams);
  };

  const formatValue = (value) => {
    return typeof value === 'number' ? value.toFixed(3) : '0.000';
  };

  const getValueColor = (parameter, value) => {
    if (!featureRanges[parameter]) return 'primary';
    
    const range = featureRanges[parameter];
    const normalized = (value - range.min) / (range.max - range.min);
    
    if (normalized < 0.3) return 'success';
    if (normalized > 0.7) return 'error';
    return 'warning';
  };

  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <Container maxWidth="lg" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
          <Box sx={{ textAlign: 'center' }}>
            <CircularProgress size={60} />
            <Typography variant="h6" sx={{ mt: 2 }}>
              Loading ML Models...
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Training models and initializing interface
            </Typography>
          </Box>
        </Container>
      </ThemeProvider>
    );
  }

  if (error) {
    return (
      <ThemeProvider theme={theme}>
        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
          <Typography variant="body1">
            To start the API server, run: <code>python api_server.py</code>
          </Typography>
        </Container>
      </ThemeProvider>
    );
  }

  const inputVariables = [
    'Speed', 'Throttle', 'Brake', 'Surface_Roughness',
    'front_surface_temp', 'rear_surface_temp', 'force_on_tire'
  ];

  const outputVariables = [
    'Tire_wear', 'Tire degreadation', 'cumilative_Tire_Wear'
  ];

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
          🚗 ML Parameter Impact Analyzer
        </Typography>
        
        <Typography variant="subtitle1" align="center" color="text.secondary" sx={{ mb: 4 }}>
          Adjust any parameter and see how all others respond in real-time using trained ML models
        </Typography>

        <Grid container spacing={3}>
          {/* Input Parameters */}
          <Grid item xs={12} md={8}>
            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h5" gutterBottom color="primary">
                🎛️ Input Parameters
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Adjust these values to see their impact on tire wear metrics
              </Typography>
              
              <Grid container spacing={3}>
                {inputVariables.map((param) => (
                  <Grid item xs={12} sm={6} key={param}>
                    <Card variant="outlined">
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                          <Typography variant="h6" component="div">
                            {param.replace(/_/g, ' ')}
                          </Typography>
                          <Chip 
                            label={formatValue(parameters[param])} 
                            color={getValueColor(param, parameters[param])}
                            variant="filled"
                          />
                        </Box>
                        
                        {featureRanges[param] && (
                          <Box sx={{ px: 1 }}>
                            <Slider
                              value={parameters[param] || featureRanges[param].median}
                              min={featureRanges[param].min}
                              max={featureRanges[param].max}
                              step={(featureRanges[param].max - featureRanges[param].min) / 100}
                              onChange={(e, newValue) => handleParameterChange(param, newValue)}
                              valueLabelDisplay="auto"
                              valueLabelFormat={(value) => formatValue(value)}
                            />
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                              <Typography variant="caption" color="text.secondary">
                                Min: {formatValue(featureRanges[param].min)}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                Max: {formatValue(featureRanges[param].max)}
                              </Typography>
                            </Box>
                          </Box>
                        )}
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Paper>
          </Grid>

          {/* Output Predictions */}
          <Grid item xs={12} md={4}>
            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h5" gutterBottom color="secondary">
                📊 Tire Wear Predictions
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                ML model predictions based on current parameters
              </Typography>
              
              {outputVariables.map((param) => (
                <Card variant="outlined" sx={{ mb: 2 }} key={param}>
                  <CardContent>
                    <Typography variant="h6" component="div" gutterBottom>
                      {param.replace(/_/g, ' ')}
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="h4" component="div" color="primary">
                        {formatValue(predictions[param])}
                      </Typography>
                      <Chip 
                        label={predictions[param] > (featureRanges[param]?.mean || 0) ? "High" : "Low"}
                        color={predictions[param] > (featureRanges[param]?.mean || 0) ? "error" : "success"}
                        size="small"
                      />
                    </Box>
                    {featureRanges[param] && (
                      <Typography variant="caption" color="text.secondary">
                        Range: {formatValue(featureRanges[param].min)} - {formatValue(featureRanges[param].max)}
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              ))}
            </Paper>

            {/* Quick Stats */}
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                🎯 Quick Insights
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Chip 
                  label={`Speed: ${formatValue(parameters.Speed)} mph`}
                  color="primary" 
                  variant="outlined"
                />
                <Chip 
                  label={`Tire Wear: ${formatValue(predictions.Tire_wear)}`}
                  color={predictions.Tire_wear > 0.5 ? "error" : "success"}
                  variant="outlined"
                />
                <Chip 
                  label={`Temperature: ${formatValue(parameters.front_surface_temp)}°F`}
                  color={parameters.front_surface_temp > 120 ? "error" : "success"}
                  variant="outlined"
                />
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </ThemeProvider>
  );
}

export default App;