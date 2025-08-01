/**
 * Loading screen component
 */
import React from 'react';
import {
  Container,
  Box,
  CircularProgress,
  Typography
} from '@mui/material';

const LoadingScreen = ({ message = "Loading ML Models...", subtitle = "Training models and initializing interface" }) => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, display: 'flex', justifyContent: 'center' }}>
      <Box sx={{ textAlign: 'center' }}>
        <CircularProgress size={60} />
        <Typography variant="h6" sx={{ mt: 2 }}>
          {message}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {subtitle}
        </Typography>
      </Box>
    </Container>
  );
};

export default LoadingScreen;