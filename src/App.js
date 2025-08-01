/**
 * Clean Architecture Main Application Component
 */
import React from 'react';
import {
  Container,
  Typography,
  Grid,
  Paper,
  Box,
  Chip,
  Button
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import RefreshIcon from '@mui/icons-material/Refresh';

// Custom hooks and services
import { useMLPredictions } from './frontend/hooks/useMLPredictions';

// Components
import ParameterSlider from './frontend/components/ParameterSlider';
import PredictionCard from './frontend/components/PredictionCard';
import LoadingScreen from './frontend/components/LoadingScreen';
import ErrorScreen from './frontend/components/ErrorScreen';

// Types and utilities
import { INPUT_VARIABLES, OUTPUT_VARIABLES } from './frontend/types';
import { formatValueWithUnit } from './frontend/utils/formatters';
import config from './frontend/utils/config';

const theme = createTheme({
  palette: {
    primary: {
      main: config.THEME.PRIMARY,
    },
    secondary: {
      main: config.THEME.SECONDARY,
    },
    background: {
      default: config.THEME.BACKGROUND,
    },
  },
});

function App() {
  const {
    parameters,
    predictions,
    featureRanges,
    loading,
    error,
    initialized,
    updateParameter,
    resetParameters,
    retry
  } = useMLPredictions();

  // Loading state
  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <LoadingScreen />
      </ThemeProvider>
    );
  }

  // Error state
  if (error) {
    return (
      <ThemeProvider theme={theme}>
        <ErrorScreen error={error} onRetry={retry} />
      </ThemeProvider>
    );
  }

  // Main application interface
  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center" sx={{ mb: 4 }}>
          🚗 Analisador de Impacto de Parâmetros ML
        </Typography>
        
        <Typography variant="subtitle1" align="center" color="text.secondary" sx={{ mb: 4 }}>
          Ajuste qualquer parâmetro e veja como todos os outros respondem em tempo real usando modelos ML treinados
        </Typography>

        <Grid container spacing={3}>
          {/* Input Parameters */}
          <Grid item xs={12} md={8}>
            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h5" color="primary">
                  🎛️ Parâmetros de Entrada
                </Typography>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={resetParameters}
                  startIcon={<RefreshIcon />}
                >
                  Resetar Padrões
                </Button>
              </Box>
              
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Ajuste estes valores para ver seu impacto nas métricas de desgaste do pneu
              </Typography>
              
              <Grid container spacing={3}>
                {INPUT_VARIABLES.map((param) => (
                  <Grid item xs={12} sm={6} key={param}>
                    <ParameterSlider
                      parameter={param}
                      value={parameters[param]}
                      featureRange={featureRanges[param]}
                      onChange={updateParameter}
                      disabled={!initialized}
                    />
                  </Grid>
                ))}
              </Grid>
            </Paper>
          </Grid>

          {/* Output Predictions */}
          <Grid item xs={12} md={4}>
            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h5" gutterBottom color="secondary">
                📊 Previsões de Desgaste do Pneu
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Previsões do modelo ML baseadas nos parâmetros atuais
              </Typography>
              
              {OUTPUT_VARIABLES.map((param) => (
                <PredictionCard
                  key={param}
                  parameter={param}
                  value={predictions[param]}
                  featureRange={featureRanges[param]}
                />
              ))}
            </Paper>

            {/* Quick Insights */}
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                🎯 Insights Rápidos
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Chip 
                  label={`Velocidade: ${formatValueWithUnit(parameters.Speed, 'Speed')}`}
                  color="primary" 
                  variant="outlined"
                />
                <Chip 
                  label={`Desgaste: ${formatValueWithUnit(predictions.Tire_wear, 'Tire_wear')}`}
                  color={predictions.Tire_wear > 0.5 ? "error" : "success"}
                  variant="outlined"
                />
                <Chip 
                  label={`Temperatura: ${formatValueWithUnit(parameters.front_surface_temp, 'front_surface_temp')}`}
                  color={parameters.front_surface_temp > 60 ? "error" : "success"}
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