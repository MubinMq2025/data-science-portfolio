
# Panel Degradation Detection System

## Overview

This project presents a machine learning-based Panel Degradation Detection System developed as part of the Omni-Grid Renewable Energy Intelligence Platform.

The prototype is designed to identify gradual solar panel efficiency decline and long-term operational underperformance using SCADA telemetry, environmental variables, thermal stress indicators, and historical operational behaviour.

The system combines weather-normalised degradation modelling, residual analysis, rolling trend detection, and XGBoost-based machine learning to simulate proactive renewable energy asset monitoring and maintenance planning workflows.

---

# Objectives

The primary objectives of this project are to:

* Detect long-term solar panel degradation
* Identify persistent underperformance patterns
* Simulate proactive maintenance recommendation workflows
* Analyse operational degradation drivers
* Demonstrate explainable AI techniques for renewable energy systems
* Build a scalable prototype for AI-driven solar asset intelligence

---

# Key Features

* Synthetic degradation simulation
* Feature engineering and rolling degradation indicators
* XGBoost regression modelling
* Residual error analysis
* Degradation severity classification
* Feature importance analysis
* SHAP explainability
* Operational maintenance recommendation logic
* Final operational output generation
* Visual analytics and model evaluation

---

# Dataset

The prototype uses a synthetic SCADA-style renewable energy dataset containing:

* Operational telemetry
* Environmental variables
* Thermal indicators
* Electrical stability features
* Efficiency metrics
* Historical degradation indicators

### Example Features

| Category      | Features                                                 |
| ------------- | -------------------------------------------------------- |
| Environmental | Ambient temperature, humidity, UV exposure, dust soiling |
| Operational   | Efficiency percentage, restart counts, error counts      |
| Thermal       | Internal temperature, thermal cycling                    |
| Electrical    | Voltage ripple, harmonic distortion                      |
| Historical    | Rolling efficiency means, degradation trends             |

---

# Modelling Approach

The project follows a weather-normalised degradation detection workflow:

1. Generate synthetic degradation behaviour
2. Engineer operational and degradation-related features
3. Train an XGBoost regression model
4. Predict degradation scores
5. Perform residual analysis
6. Convert scores into operational severity levels
7. Generate maintenance recommendations

---

# Machine Learning Models

## XGBoost Regressor

The primary model used for degradation score prediction.

### Why XGBoost?

* Handles nonlinear relationships effectively
* Performs well on structured SCADA data
* Robust against noisy operational telemetry
* Supports feature importance analysis
* Highly scalable for industrial ML systems

---

# Evaluation Metrics

The model is evaluated using:

| Metric    | Purpose                                        |
| --------- | ---------------------------------------------- |
| MAE       | Average prediction error                       |
| RMSE      | Penalises larger prediction errors             |
| R² Score  | Measures explained variability                 |
| MAPE      | Percentage forecasting error                   |
| Precision | Classification accuracy for degradation alerts |
| Recall    | Detection coverage of degradation events       |
| F1 Score  | Balance between precision and recall           |

---

# Key Results

The prototype achieved:

* Strong degradation trend prediction capability
* R² score of approximately 0.71
* Low residual bias
* Realistic degradation severity distribution
* Explainable feature importance outputs

### Top Degradation Drivers

* Efficiency percentage
* Internal temperature
* Thermal stress index
* Rolling efficiency decline indicators
* Voltage ripple and electrical instability

---

# Visualisations Included

The notebook contains:

* Actual vs Predicted degradation plots
* Residual error distributions
* Feature importance charts
* Severity distribution analysis
* SHAP explainability visualisations
* Confusion matrix for degradation severity classification

---

# SHAP Explainability

SHAP analysis is used to interpret model predictions and identify how operational variables contribute to degradation risk.

This improves:

* Model transparency
* Operational interpretability
* Trustworthiness of AI outputs
* Renewable energy analytics explainability

---

# Operational Output

The final output includes:

* Degradation score
* Severity classification
* Maintenance recommendation
* Operational monitoring format
* Export-ready CSV results

---

# Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Matplotlib
* Seaborn
* SHAP
* Jupyter Notebook

---

# Project Structure

```text
Panel-Degradation-Detection/
│
├── panel_degradation_prototype.ipynb
├── panel_degradation_results.csv
├── README.md
├── requirements.txt
└── assets/
    ├── feature_importance.png
    ├── residual_distribution.png
    ├── degradation_distribution.png
    └── shap_summary.png
```

---

# Future Improvements

Potential future enhancements include:

* Real-world SCADA deployment
* Real-time streaming analytics
* Deep learning time-series models
* Drone-assisted thermal inspection
* Computer vision crack detection
* Digital twin integration
* Cloud-native deployment architecture
* Edge AI inference for solar farms

---

# Disclaimer

This project uses synthetic operational data for prototyping and demonstration purposes. The workflow is designed to simulate realistic renewable energy asset monitoring and degradation analytics scenarios.

---

# Author

Kazi Abdul Mubin

Master of Data Science
Macquarie University
AIROBOD Internship Project – Omni-Grid Platform
