# Solar Forecasting System

A hybrid machine learning model for forecasting solar energy generation using time-series and weather data.

---

## Overview

This module focuses on predicting solar energy output using a combination of deep learning and ensemble methods. Accurate forecasting is essential for optimising energy distribution and grid stability in renewable energy systems.

---

## Problem Statement

Solar energy generation is highly dependent on weather conditions and temporal patterns. Traditional models struggle to capture both:

- Long-term temporal dependencies  
- Non-linear relationships in weather data  

This module addresses these challenges using a hybrid modelling approach.

---

## Data

- Simulated weather data (temperature, irradiance, humidity)
- Time-based features (hour, day, seasonal patterns)

---

## Methodology

### Feature Engineering
- Lag features and rolling statistics  
- Time-based variables (hour of day, day of week)  
- Weather-based indicators  

---

### Models Used

- **Temporal Fusion Transformer (TFT)** → captures long-term temporal dependencies  
- **XGBoost** → handles non-linear feature interactions  

---

## Results

- Achieved robust predictive performance across simulated time-series scenarios  
- Improved stability and accuracy compared to single-model approaches  

---

## Visualisations

- Forecast vs Actual plots  
- Feature importance analysis  
- Time-series trend visualisations  

---

## Key Takeaways

- Hybrid models improve forecasting accuracy  
- Time-series feature engineering is critical  
- Combining deep learning and boosting yields strong performance  

---