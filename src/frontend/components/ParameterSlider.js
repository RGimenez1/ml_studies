/**
 * Reusable parameter slider component
 */
import React from 'react';
import {
  Card,
  CardContent,
  Slider,
  Typography,
  Box,
  Chip
} from '@mui/material';
import { formatValueWithUnit, formatParameterName, getValueColor, getSliderStep } from '../utils/formatters';

const ParameterSlider = ({ 
  parameter, 
  value, 
  featureRange, 
  onChange,
  disabled = false 
}) => {
  if (!featureRange) return null;

  const handleChange = (event, newValue) => {
    onChange(parameter, newValue);
  };

  return (
    <Card variant="outlined">
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" component="div">
            {formatParameterName(parameter)}
          </Typography>
          <Chip 
            label={formatValueWithUnit(value, parameter)} 
            color={getValueColor(parameter, value, { [parameter]: featureRange })}
            variant="filled"
          />
        </Box>
        
        <Box sx={{ px: 1 }}>
          <Slider
            value={value || featureRange.median}
            min={featureRange.min}
            max={featureRange.max}
            step={getSliderStep(featureRange.min, featureRange.max)}
            onChange={handleChange}
            valueLabelDisplay="auto"
            valueLabelFormat={(value) => formatValueWithUnit(value, parameter)}
            disabled={disabled}
          />
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
            <Typography variant="caption" color="text.secondary">
              Min: {formatValueWithUnit(featureRange.min, parameter)}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Max: {formatValueWithUnit(featureRange.max, parameter)}
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ParameterSlider;