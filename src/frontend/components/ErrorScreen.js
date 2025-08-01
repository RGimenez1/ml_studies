/**
 * Error screen component
 */
import React from 'react';
import {
  Container,
  Alert,
  Typography,
  Button,
  Box
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';

const ErrorScreen = ({ 
  error, 
  onRetry, 
  showRetryButton = true,
  showInstructions = true 
}) => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
      
      {showInstructions && (
        <Typography variant="body1" sx={{ mb: 2 }}>
          To start the API server, run: <code>python api_server_clean.py</code>
        </Typography>
      )}
      
      {showRetryButton && onRetry && (
        <Box sx={{ mt: 2 }}>
          <Button 
            variant="contained" 
            onClick={onRetry}
            startIcon={<RefreshIcon />}
          >
            Retry
          </Button>
        </Box>
      )}
    </Container>
  );
};

export default ErrorScreen;