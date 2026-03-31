# Statistical Inference: Simulation and Maximum Likelihood Estimation

## Overview

This project applies advanced statistical inference techniques to both simulated and real-world datasets. It focuses on:

- Evaluating estimator performance under ideal and contaminated conditions
- Applying Monte Carlo simulation to quantify bias, variance, and error
- Implementing Maximum Likelihood Estimation (MLE) for logistic regression
- Analysing uncertainty using Fisher Information and profile likelihood

The project demonstrates how statistical methods can be used to handle real-world data challenges such as skewness, outliers, and model uncertainty.

---

## Why This Project Matters

In practical data science, datasets are rarely clean. This project highlights:

- How **outliers can completely break standard estimators**
- Why **robust statistics are critical in production systems**
- How **MLE provides interpretable and scalable modelling frameworks**
- How statistical models can inform **real-world policy decisions (UNSDG Goal 3)**

---

## Technologies & Methods

- **Programming:** R, Quarto  
- **Libraries:** dplyr, ggplot2, gapminder  
- **Techniques:**
  - Monte Carlo simulation (1000 replications)
  - Bias–variance decomposition
  - Robust estimation (median, trimmed mean)
  - Maximum Likelihood Estimation (MLE)
  - Logistic regression
  - Fisher Information (Hessian-based inference)
  - Confidence intervals (Wald)
  - Profile likelihood analysis

---

# Section 1: Simulation-Based Inference

## Objective

Evaluate estimator performance for **typical completion time** under:

- Clean data (Exponential distribution)
- Contaminated data (outliers introduced)

---

## Contaminated Sample Behaviour

Example simulated outputs:

mean median trimmed_mean
6.0096 0.8407 1.1078
5.7869 0.8382 1.1120
5.8428 0.7877 0.9839


👉 The mean explodes due to extreme values, while median remains stable.

---

## Monte Carlo Results (Contaminated Data)

| Estimator        | Bias   | MCSD  | MSE   |
|-----------------|--------|------|------|
| Mean            | 4.9373 | 1.3813 | 26.2825 |
| Median          | -0.1871 | 0.0821 | 0.0417 |
| Trimmed Mean    | 0.1163 | 0.1686 | 0.0419 |

---

## Key Findings

### Mean (Not Robust)
- Massive bias: **+4.937**
- Extremely high error: **MSE ≈ 26.28**
- Highly sensitive to outliers

👉 Completely unreliable in real-world noisy data

---

### Median (Most Robust)
- Very small bias: **−0.187**
- Low variability: **MCSD ≈ 0.082**
- Stable error: **MSE ≈ 0.0417**

👉 Best estimator under contamination

---

### Trimmed Mean (Balanced)
- Slight bias: **0.116**
- Moderate variability
- Similar performance to median

👉 Good compromise between efficiency and robustness

---

## Core Insight

> Outliers dramatically inflate the mean but have minimal impact on robust estimators.

This demonstrates why **robust statistics are essential in real-world analytics pipelines**.

---

# Section 2: Maximum Likelihood Estimation (MLE)

## Objective

Predict whether a country has **above-median life expectancy** using:

- Predictor: log(GDP per capita)
- Model: Logistic regression

---

## Model Estimates

| Parameter | Estimate |
|----------|---------|
| β₀       | -20.382 |
| β₁       | 2.3489  |

- Results from `optim()` and `glm()` are **identical**
- Confirms correctness of manual MLE implementation

---

## Interpretation

- β₁ > 0 → Higher GDP increases probability of higher life expectancy
- Odds ratio:

exp(β₁) ≈ 10.5
A one-unit increase in log(GDP) multiplies odds by ~10.5×

---

## Fisher Information & Uncertainty

Variance–covariance matrix:
[11.457 -1.303]
[-1.303 0.149]


Standard errors:

- SE(β₀) ≈ 3.3848  
- SE(β₁) ≈ 0.3863  

---

## 95% Confidence Intervals

| Parameter | Lower | Estimate | Upper |
|----------|------|---------|------|
| β₀       | -27.0166 | -20.3824 | -13.7483 |
| β₁       | 1.5917 | 2.3489 | 3.1061 |

👉 Confidence interval for β₁ excludes 0 → statistically significant

---

## Profile Likelihood Analysis

- Sharp peak at β₁ ≈ 2.35  
- Steep curvature → high precision  
- Asymmetry indicates stronger penalty for larger values  

👉 Confirms stability and reliability of the estimate

---

## Real-World Interpretation

- 10% GDP increase → ~26% higher odds  
- Doubling GDP → ~5× higher odds  

👉 Strong relationship between **economic development and health outcomes**

---

## Policy Implications (UNSDG Goal 3)

Findings support investment in:

- Healthcare systems  
- Education  
- Sanitation & infrastructure  
- Public health programs  

---

## Key Skills Demonstrated

- Monte Carlo simulation  
- Bias–variance analysis  
- Robust statistical modelling  
- Handling skewed and contaminated datasets  
- Maximum Likelihood Estimation (MLE)  
- Logistic regression modelling  
- Fisher Information and uncertainty quantification  
- Profile likelihood analysis  
- Translating statistical results into policy insights  

---

## Conclusion

This project demonstrates how statistical inference techniques can be applied to:

- Evaluate estimator performance under real-world conditions  
- Build interpretable predictive models  
- Quantify uncertainty rigorously  
- Support data-driven decision making  

It highlights the importance of **robustness, efficiency, and interpretability in modern data science workflows**.
