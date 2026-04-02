# Wearable Activity Recognition using Machine Learning

## Overview
This project explores how machine learning can be used to analyse wearable IoT sensor data for **human activity recognition** and **context-aware healthcare monitoring**.

Using multimodal sensor data from wearable devices, the study evaluates multiple machine learning and deep learning models to classify human physical activities.

---

##  Objectives
- Classify human activities using wearable sensor data
- Compare performance of multiple ML models
- Identify key sensors contributing to activity recognition
- Improve interpretation of physiological signals using activity context

---

## Dataset
- **Dataset:** MHEALTH (Mobile Health Dataset)
- **Sensors Used:**
  - Accelerometer
  - Gyroscope
  - Magnetometer
  - ECG (Electrocardiogram)
- **Sensor Locations:**
  - Chest
  - Arm
  - Ankle

The dataset contains time-series sensor data collected from multiple participants performing various activities.

---

## Methodology

### Data Preprocessing
- Merged multiple participant files
- Removed null activity class (label = 0)
- Applied feature scaling (standardisation)
- Conducted exploratory data analysis

### Model Implementation
The following models were implemented:

- **K-Nearest Neighbour (KNN)** – baseline model
- **Random Forest** – ensemble learning model
- **Long Short-Term Memory (LSTM)** – deep learning for time-series data

### Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

---

## Results

| Model           | Accuracy |
|----------------|----------|
| KNN            | ~68%     |
| Random Forest  | ~79%     |
| LSTM           | ~72%     |

- Random Forest achieved the highest accuracy
- Motion sensors contributed most to performance
- ECG signals had lower importance for activity classification

---

## Key Insights
- Motion-based sensors (accelerometer & gyroscope) are the most informative
- Context-aware systems improve interpretation of physiological signals
- Ensemble models outperform both simple and deep learning models in this setup

---

## Tools & Technologies
- Python
- Pandas, NumPy
- Scikit-learn
- TensorFlow / Keras
- Matplotlib / Seaborn
- Jupyter Notebook

---

## Project Structure
1.  data
2. notebooks
3. Assignment1.ipynb
4. report
5. report.pdf
6.  README.md


---

## Business Impact
This project demonstrates how machine learning can:
- Reduce false health alerts
- Improve wearable healthcare systems
- Enable smarter real-time monitoring

---

## References
- MHEALTH Dataset
- Research papers on wearable IoT and activity recognition

---

## Author
Kazi Abdul Mubin  
Master of Data Science — Macquarie University
