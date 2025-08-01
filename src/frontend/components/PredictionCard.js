/**
 * Reusable prediction display card component
 */
import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip
} from '@mui/material';
import { formatValueWithUnit, formatParameterName, isValueHigh, getInsightLabel } from '../utils/formatters';

const PredictionCard = ({ 
  parameter, 
  value, 
  featureRange 
}) => {
  const isHigh = featureRange ? isValueHigh(value, featureRange.mean) : false;

  return (
    <Card variant="outlined" sx={{ mb: 2 }}>
      <CardContent>
        <Typography variant="h6" component="div" gutterBottom>
          {formatParameterName(parameter)}
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h4" component="div" color="primary">
            {formatValueWithUnit(value, parameter)}
          </Typography>
          <Chip 
            label={getInsightLabel(value, featureRange)}
            color={isHigh ? "error" : "success"}
            size="small"
          />
        </Box>
        {featureRange && (
          <Typography variant="caption" color="text.secondary">
            Faixa: {formatValueWithUnit(featureRange.min, parameter)} - {formatValueWithUnit(featureRange.max, parameter)}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default PredictionCard;