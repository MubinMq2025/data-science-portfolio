# Omni-Grid Predictive Analytics System

An end-to-end machine learning ecosystem for **energy forecasting, anomaly detection, and predictive maintenance** within a next-generation AI-driven platform for renewable energy infrastructure.

---

## Overview

The Omni-Grid system is designed to simulate a real-world ML platform that supports intelligent decision-making in renewable energy systems. It integrates multiple machine learning modules into a unified pipeline to:

- Forecast solar energy generation  
- Detect abnormal system behaviour  
- Predict equipment failure through Remaining Useful Life (RUL) estimation  

This project demonstrates **system-level ML thinking**, combining time-series modelling, anomaly detection, and predictive analytics within a scalable architecture.

---

## Problem Statement

Renewable energy systems rely heavily on accurate forecasting, early fault detection, and efficient maintenance planning. Traditional approaches often treat these problems separately, leading to inefficiencies.

This project addresses this gap by building an **integrated ML system** that combines:

- Forecasting for energy optimisation  
- Anomaly detection for system monitoring  
- Predictive maintenance for lifecycle management  

---

## System Architecture

The pipeline follows a modular ML architecture:

1. **Data Ingestion**
   - Simulated weather data  
   - Sensor and operational data  

2. **Data Preprocessing**
   - Data cleaning and transformation  
   - Handling missing values  

3. **Feature Engineering**
   - Time-based features (lags, rolling windows)  
   - Weather and operational indicators  

4. **Model Layer**
   - Forecasting (TFT + XGBoost)  
   - Anomaly Detection (Isolation Forest)  
   - Predictive Maintenance (Gradient Boosting)  

5. **Evaluation**
   - RMSE, MAE (forecasting)  
   - ROC-AUC (anomaly detection)  

6. **Output**
   - Energy forecasts  
   - Anomaly alerts  
   - Maintenance recommendations  

---

## Key Components

### Solar Forecasting System
- Hybrid **Temporal Fusion Transformer (TFT) + XGBoost** model  
- Time-series modelling using weather and temporal features  
- Focus on improving prediction accuracy for energy output  

---

### Anomaly Detection System
- **Isolation Forest + statistical thresholding**  
- Identifies abnormal system behaviour  
- Supports early fault detection and monitoring  

---

### Predictive Maintenance (RUL Model)
- **Gradient Boosting Regression**  
- Estimates Remaining Useful Life (RUL) of assets  
- Enables proactive maintenance planning  

---

## Technologies Used

- **Programming:** Python  
- **Libraries:** Pandas, NumPy, Scikit-learn, TensorFlow / PyTorch  
- **Machine Learning:** XGBoost, Random Forest, LSTM, Isolation Forest  
- **Explainability:** SHAP  
- **Concepts:** Time-Series Analysis, Feature Engineering, Model Evaluation  
- **Cloud (Conceptual):** Azure, AWS  

---

## Results & Evaluation

Models were evaluated using standard metrics:

- **Forecasting:** RMSE, MAE  
- **Anomaly Detection:** ROC-AUC  
- **Predictive Maintenance:** Regression-based evaluation metrics  

The system demonstrates **robust predictive performance across simulated scenarios**, validating the effectiveness of the integrated pipeline.

---

## Note on Data

This project uses **synthetic and simulated datasets** to replicate real-world conditions.

This approach was taken to:
- Maintain confidentiality in an industry-inspired setting  
- Focus on validating system architecture and modelling techniques  

---

## Repository Structure
omni-grid-ml-system/
│
├── solar-forecasting/
├── anomaly-detection/
├── predictive-maintenance/
├── pipeline-architecture/
└── README.md


Each module contains its own implementation, analysis, and documentation.

---

## Key Learnings

- Designing **end-to-end ML pipelines**  
- Integrating multiple ML models into a unified system  
- Applying **time-series modelling and anomaly detection**  
- Using **SHAP for model interpretability**  
- Structuring scalable, production-like ML architectures  

---

## Future Improvements

- Integration with real-world datasets  
- Model deployment using cloud platforms  
- Real-time data streaming and monitoring  
- Dashboard integration for visual analytics  

---

## Author

**Kazi Abdul Mubin**  
Master of Data Science — Macquarie University  

- [LinkedIn](https://www.linkedin.com/in/kazi-abdul-mubin-919041280/)  
- [GitHub](https://github.com/MubinMq2025)

---