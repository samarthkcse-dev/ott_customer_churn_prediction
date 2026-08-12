# 🎬 OTT Customer Churn Prediction using Machine Learning

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Project Overview

OTT platforms like Netflix, JioHotstar, Amazon Prime Video, and Disney+ lose customers due to subscription cancellations (customer churn). This project predicts whether a customer is likely to churn using Machine Learning and provides an easy-to-use web interface for predictions.

The project demonstrates the complete Data Science workflow, including data preprocessing, analysis, visualization, machine learning model training, and deployment using Streamlit.

---

## 🎯 Objectives

- Predict whether a customer will churn.
- Analyze customer behavior and subscription patterns.
- Identify important factors affecting churn.
- Help OTT businesses improve customer retention.

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- MySQL
- Streamlit
- Joblib
- Git & GitHub

---

## 📂 Project Structure

```
OTT_Customer_Churn_Prediction/
│
├── data/
│   ├── customers.csv
│   └── churn_dataset.csv
│
├── notebooks/
│   └── data_analysis.ipynb
│
├── model_training.py
├── app.py
├── model.pkl
├── requirements.txt
├── README.md
│
└── images/
    ├── dashboard.png
    └── prediction.png
```

---

## ⚙️ Workflow

1. Collect customer dataset.
2. Clean and preprocess data.
3. Perform Exploratory Data Analysis (EDA).
4. Encode categorical features.
5. Train the Random Forest model.
6. Save the trained model.
7. Build a Streamlit web application.
8. Predict customer churn from user input.

---

## 📊 Exploratory Data Analysis (EDA)

- Missing value handling
- Duplicate removal
- Churn distribution
- Subscription plan analysis
- Device-wise analysis
- Monthly watch hours analysis
- Correlation analysis

---

## 🤖 Machine Learning Model

**Algorithm:** Random Forest Classifier

**Steps:**

- Feature Selection
- Train-Test Split
- Model Training
- Prediction
- Model Evaluation

---

## 📈 Visualizations

- Churn Distribution
- Subscription Plan Comparison
- Device Usage
- Monthly Watch Hours
- Correlation Heatmap
- Feature Importance

---

## 💾 SQL Analysis

Example business queries:

- Total customers
- Total churned customers
- Churn rate
- Plan-wise churn
- Device-wise churn
- Average watch hours
- Monthly revenue analysis
- Region-wise customer distribution

---

## 🌐 Streamlit Application

The web application allows users to:

- Enter customer information
- Predict customer churn
- Display prediction result instantly
- Provide a simple and interactive interface

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the Model

```bash
python model_training.py
```

### 3. Run the Application

```bash
streamlit run app.py
```

---

## 📊 Sample Prediction

**Input**

| Feature | Value |
|---|---|
| Age | 28 |
| Subscription Plan | Premium |
| Monthly Watch Hours | 65 |
| Devices Used | 3 |

**Prediction**

> ✅ Customer will **NOT** Churn

---

## 📌 Future Improvements

- AI-powered churn explanation
- Customer retention recommendations
- Interactive dashboard
- Email notification system
- Cloud deployment
- Real-time database integration

---

## 👨‍💻 Author

**Samarth Siddharam Kore**
Diploma in Computer Engineering

---

## ⭐ Acknowledgements

- Scikit-learn
- Streamlit
- Pandas
- NumPy
- Matplotlib
- MySQL
- Open Source Community
