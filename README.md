# 🎬 OTT Customer Churn & Retention Intelligence Suite

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Multipage-red)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Random%20Forest%20(96.4%25)-orange)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-blueviolet)
![Gemini AI](https://img.shields.io/badge/GenAI-Google%20Gemini-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Project Overview

Streaming platforms like Netflix, Disney+, and Amazon Prime Video lose substantial recurring revenue to subscriber cancellations (churn). 

This enterprise-grade intelligence platform predicts subscriber churn risk with a **96.4% accurate Random Forest model**, provides real-time **interactive "What-If" sensitivity simulations**, visualizes portfolio-level risk with **interactive Plotly analytics**, and generates automated retention campaigns via **Google Gemini GenAI**.

---

## 🚀 Key Modules (Multipage Application)

* **🏠 Home / Overview Command Center:** Live platform KPI counters (Subscribers, MRR, Platform Churn Rate) and module launchpad.
* **🎯 1. Real-Time Customer Predictor:**
  * **Instant Showcase Presets:** 1-click loading for At-Risk Dormant, Loyal Family, Borderline, and Student personas.
  * **Interactive Speedometer Gauge:** Dynamic color-coded churn risk meter (Safe / Moderate / Critical).
  * **"What-If" Sensitivity Simulator:** Real-time risk recalculation when testing price discounts, auto-renewal incentives, or watch-time boosts.
  * **Gemini AI Retention Copilot:** Root cause analysis, business intervention plan, and tailored outreach email/push notification.
* **📂 2. Batch Cohort Analysis:**
  * Ingest CSV portfolios or load a pre-configured 150-subscriber demo cohort.
  * Portfolio risk segmentation donut chart, plan-wise churn breakdowns, and Monthly Revenue at Risk ($MRR).
  * 1-click enriched CSV download with churn scores and risk categories.
* **📊 3. Executive Streaming Dashboard:**
  * Segment filtering by Subscription Plan, Primary Device, and Senior Demographics across 9,476 platform records.
  * Behavioral analysis (Login inactivity gap vs churn, watch hours distribution).
  * SQL Query Showcase highlighting business queries and outputs executed on MySQL database.
* **🧠 4. Model Intelligence & Explainability (XAI):**
  * Random Forest architecture scorecard (96.4% Accuracy, 0.986 ROC-AUC, 97% Recall).
  * Global feature importance chart highlighting `days_since_last_login` (51.4%) as the primary attrition driver.
  * Interactive Confusion Matrix heatmap and benchmark comparison table against Decision Trees and Logistic Regression.

---

## 🛠️ Tech Stack

* **Machine Learning:** Scikit-learn (Random Forest Classifier), Joblib
* **Generative AI:** Google Gemini API (`google-genai`)
* **Visualization:** Plotly Graph Objects & Express, Matplotlib
* **Web Architecture:** Streamlit Multipage Framework
* **Data Processing:** Pandas, NumPy
* **Database & SQL:** MySQL

---

## 📂 Project Structure

```
OTT_Customer_Churn_Prediction/
│
├── Home.py                       # Main Executive Command Center
├── app.py                        # Application entrypoint
├── app2.py                       # Standalone single-page predictor with AI
│
├── pages/                        # Multipage modules
│   ├── 1_🎯_Customer_Predictor.py
│   ├── 2_📂_Batch_Prediction.py
│   ├── 3_📊_Executive_Dashboard.py
│   └── 4_🧠_Model_Intelligence.py
│
├── utils/                        # Shared utility modules
│   ├── model_loader.py           # Cached model, dataset loaders & personas
│   └── ui_components.py          # Custom CSS, Plotly charts & Gemini copilot
│
├── Data/
│   ├── Cleaned Data/             # Cleaned user dataset (9,476 rows)
│   └── *.csv                     # Raw platform logs (watch, search, reviews)
│
├── models/
│   ├── cust_churn_model.pkl      # Trained Random Forest Model
│   ├── encoder.pkl               # Label Encoders
│   └── features.pkl              # 12 Model Features List
│
├── SQL/                          # MySQL Queries
├── Visualizations/               # Power BI & Matplotlib notebooks
├── .env.example                  # Environment configuration template
└── requirements.txt              # Project dependencies
```

---

## ⚙️ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment (Optional for GenAI)
Copy `.env.example` to `.env` and add your Google Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Note: If no API key is set, the app automatically uses intelligent rule-based retention strategies.)*

### 3. Launch Application
```bash
streamlit run Home.py
# or
streamlit run app.py
```

---

## 👨‍💻 Author

**Samarth Siddharam Kore**  
Diploma in Computer Engineering
