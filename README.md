# Cybersecurity Intrusion Blindspot

A Machine Learning-based Network Intrusion Detection System (NIDS) developed during the **ICFOSS Internship** to detect malicious network traffic and support cybersecurity monitoring through real-time threat analysis.

---

## Internship Project

**Organization:** International Centre for Free and Open Source Solutions (ICFOSS)

**Project Title:** Network Intrusion Blindspot – Machine Learning-Based Intrusion Detection System

**Objective:**
Develop a Network Intrusion Detection System capable of analyzing network traffic and identifying malicious activities using machine learning techniques. The system aims to assist security teams in detecting threats, reducing response time, and improving network security visibility.

---

## Overview

Cybersecurity Intrusion Blindspot is an intelligent intrusion detection system that classifies network traffic as either **Normal** or **Attack** using an XGBoost machine learning model.

The application provides:

* Real-time traffic analysis
* Threat classification
* Risk assessment
* Model performance visualization
* Feature importance analysis
* Interactive cybersecurity dashboard

---

## Key Features

* Real-time network traffic classification
* XGBoost-based machine learning model
* Interactive cybersecurity-themed interface
* Threat confidence scoring
* Risk level assessment
* Feature importance visualization
* Confusion matrix analysis
* Model performance dashboard
* Streamlit-powered web application

---

## Dataset Features

The model uses the following network traffic attributes:

* Protocol
* Source Port
* Destination Port
* Bytes Sent
* Bytes Received
* User Agent
* Internal Traffic Indicator

Target Variable:

* Label

  * 0 → Normal Traffic
  * 1 → Attack Traffic

---

## Machine Learning Model

**Algorithm:** XGBoost Classifier

### Why XGBoost?

* High classification accuracy
* Handles mixed feature types efficiently
* Robust against overfitting
* Provides feature importance analysis
* Suitable for cybersecurity datasets

---

## Model Performance

| Metric    | Score  |
| --------- | ------ |
| Accuracy  | 96.65% |
| Precision | 58%    |
| Recall    | 60%    |
| F1 Score  | 59%    |

### Confusion Matrix

|               | Predicted Normal | Predicted Attack |
| ------------- | ---------------- | ---------------- |
| Actual Normal | 1885             | 35               |
| Actual Attack | 32               | 48               |

---

## Feature Importance

The most influential features identified by the model include:

* User Agent
* Destination Port
* Source Port
* Bytes Sent
* Bytes Received
* Protocol
* Internal Traffic Flag

The feature importance analysis helps explain how the model differentiates between normal and malicious traffic.

---

## Technology Stack

### Programming Language

* Python

### Machine Learning

* XGBoost
* Scikit-learn

### Data Processing

* Pandas
* NumPy

### Visualization

* Plotly
* Matplotlib

### Web Application

* Streamlit

### Model Serialization

* Joblib

---

## Project Structure

```text
Cybersecurity_Intrusion_Blindspot_Internship/

├── backend/
│
├── frontend/
│   ├── app.py
│   ├── pages/
│   └── utils/
│
├── models/
│   ├── xgboost_model.pkl
│   └── label_encoders.pkl
│
├── requirements.txt
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Jwl06/Cybersecurity_Intrusion_Blindspot_Internship.git
```

### Navigate to Project

```bash
cd Cybersecurity_Intrusion_Blindspot_Internship
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run frontend/app.py
```

---

## Application Modules

### Home

* Project overview
* Performance highlights
* Navigation interface

### Traffic Analysis

* Network traffic input form
* Attack simulation scenarios
* Real-time prediction results
* Threat risk assessment

### Dashboard

* Accuracy metrics
* Precision, Recall, F1 Score
* Feature importance chart
* Confusion matrix visualization

---

## Operational Benefits

* Early threat detection
* Faster incident response
* Reduced manual monitoring effort
* Improved network visibility
* Enhanced cybersecurity awareness
* Data-driven security analysis

---

## Future Enhancements

* Multi-class attack classification
* Live packet capture integration
* Network traffic streaming
* Automated alert generation
* SIEM integration
* Advanced threat intelligence support
* Real-time monitoring dashboard

## Acknowledgement

This project was developed as part of the **ICFOSS Internship** and demonstrates the application of Machine Learning techniques in Cybersecurity for Network Intrusion Detection and Threat Analysis.
