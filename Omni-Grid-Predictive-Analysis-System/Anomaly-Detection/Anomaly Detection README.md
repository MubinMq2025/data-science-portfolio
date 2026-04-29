# Inverter Anomaly Detection System

## Overview

This project develops a prototype anomaly detection system for solar inverter telemetry using a synthetic predictive maintenance dataset.

The objective is to identify early signs of abnormal inverter behaviour before failure occurs. The system is designed as an early warning mechanism to support proactive maintenance, reduce downtime, and improve operational efficiency.

Model performance is evaluated using ROC-AUC, which is appropriate for imbalanced anomaly detection problems.

---

## Key Features

- Early anomaly detection using near-term failure indicators  
- ROC-AUC based evaluation for imbalanced data  
- Hybrid modelling approach:
  - Unsupervised model: Isolation Forest  
  - Supervised benchmark: Random Forest  
- Temporal train-test split to prevent data leakage  
- Feature importance analysis for interpretability  
- End-to-end prototype pipeline from data preparation to evaluation  

---

## Problem Framing

Anomalies are defined based on near-term failure signals rather than observed failure events.
is_anomaly = 1 → failure within 7 days
is_anomaly = 0 → normal behaviour

This allows the model to act as an early warning system rather than a reactive failure detector.

---

## Dataset

The project uses a synthetic predictive maintenance dataset designed to simulate solar inverter behaviour.

### Data includes:
- Environmental conditions (temperature, humidity, UV exposure)  
- Operational metrics (efficiency, runtime, power output)  
- Electrical signals (voltage ripple, harmonic distortion)  
- Degradation indicators (capacitor health, thermal stress)  
- Failure-related signals and remaining useful life  

Note: Synthetic data is used to enable development while real operational data is still being collected.

---

## Methodology

### Data Preparation
- Created anomaly label using `failure_within_7d`  
- Removed leakage-prone variables  
- Encoded categorical features  

### Train-Test Split
- Used temporal split instead of random split  
- Model is trained on past data and evaluated on future data  
- Prevents data leakage and reflects real-world deployment  

### Models

**Isolation Forest (Primary Model)**  
- Learns normal behaviour patterns  
- Generates anomaly scores  
- Does not require labels during training  

**Random Forest (Benchmark Model)**  
- Supervised classifier  
- Used for comparison and interpretability  

---

## Evaluation

Primary metric:
- ROC-AUC  
  Measures how well the model ranks anomalous observations above normal ones  

Additional metrics:
- Precision  
- Recall  
- F1 Score  

---

## Results

- The model is able to separate high-risk inverter behaviour from normal operation  
- ROC-AUC indicates meaningful ranking performance  
- Feature importance highlights key drivers of anomaly risk, including:
  - Efficiency degradation  
  - Temperature behaviour  
  - Electrical instability  
  - Error frequency  

---

## Key Insights

- Thermal stress and efficiency decline are strong indicators of abnormal behaviour  
- Electrical irregularities often appear before failure  
- Frequent restarts and error spikes are associated with increased risk  

---

## Next Steps

- Tune anomaly detection threshold  
- Introduce XGBoost for fault classification  
- Add SHAP-based explainability  
- Validate with real inverter telemetry data  
- Extend into a real-time monitoring pipeline  

---

## Tech Stack

- Python  
- Pandas  
- NumPy  
- Scikit-learn  
- Matplotlib  

---

## Notes

This project is a prototype developed to simulate real-world anomaly detection workflows in solar energy systems. The approach is designed to scale to production systems once real data becomes available.

---

## Contact

For questions or collaboration, please reach out.
