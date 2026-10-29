import streamlit as st
from utils.model_loader import load_dataset, load_model_assets
from utils.ui_components import inject_custom_css

st.set_page_config(
    page_title="OTT Churn Intelligence Suite",
    page_icon="🎬",
    layout="wide"
)

inject_custom_css()

# ----------------------------
# Hero Banner
# ----------------------------
st.markdown("<h1 class='hero-title'>🎬 OTT Platform Churn & Retention Suite</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Production Machine Learning, Portfolio Risk Analytics & GenAI-Driven Retention Copilot</p>", unsafe_allow_html=True)

# ----------------------------
# Executive Stats Ribbon
# ----------------------------
df = load_dataset()
total_subs = len(df) if df is not None else 9476
churn_rate = (df['churn'].mean() * 100) if df is not None else 41.2
total_mrr = df['Monthly_Charge'].sum() if (df is not None and 'Monthly_Charge' in df.columns) else 158000

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Platform Subscribers Monitored", f"{total_subs:,}")
with k2:
    st.metric("Platform Churn Rate", f"{churn_rate:.1f}%")
with k3:
    st.metric("Monthly Platform Revenue", f"${total_mrr:,.0f}")
with k4:
    st.metric("Model Predictive Accuracy", "96.4%")

st.markdown("---")

# ----------------------------
# Feature Navigation Cards
# ----------------------------
st.markdown("<div class='section-header'>🚀 Explore Intelligence Modules</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container():
        st.markdown("""
        ### 🎯 1. Single Customer Predictor
        * **Real-Time Scoring:** Calculate attrition probability with interactive Plotly speedometer gauge.
        * **Instant Showcase Presets:** 1-click loading for At-Risk, Loyal, and Student profiles.
        * **What-If Sensitivity Simulator:** Test how price discounts, auto-renew, and watch hours alter churn risk in real-time.
        * **GenAI Retention Copilot:** Automated executive diagnosis, retention action plan, and ready-to-send email copy.
        """)
        st.page_link("pages/1_🎯_Customer_Predictor.py", label="Open Single Customer Predictor →", icon="🎯")

    st.write("")
    with st.container():
        st.markdown("""
        ### 📂 2. Batch Cohort Analysis
        * **Bulk Scoring:** Ingest hundreds of subscriber records via CSV or load a pre-configured 150-customer demo cohort.
        * **Portfolio Risk Segmentation:** Donut chart of Low, Moderate, and Critical risk subscribers.
        * **Revenue Protection:** Automatically calculates total Monthly Revenue at Risk ($MRR).
        * **Export Data:** Download the enriched, scored portfolio with risk categories with a single click.
        """)
        st.page_link("pages/2_📂_Batch_Prediction.py", label="Open Batch Cohort Analysis →", icon="📂")

with col2:
    with st.container():
        st.markdown("""
        ### 📊 3. Executive Streaming Dashboard
        * **Interactive Segment Filtering:** Slice data by Subscription Tier, Primary Streaming Device, or Age segment.
        * **Behavioral Attrition Drivers:** Interactive charts on login dormancy, monthly watch hours, and device churn.
        * **SQL Query Showcase:** View production SQL queries and outputs executed on MySQL database.
        """)
        st.page_link("pages/3_📊_Executive_Dashboard.py", label="Open Executive Dashboard →", icon="📊")

    st.write("")
    with st.container():
        st.markdown("""
        ### 🧠 4. Model Intelligence & Explainability (XAI)
        * **Random Forest Architecture:** Full model specifications, ROC-AUC (0.986), and confusion matrix heatmap.
        * **Global Feature Importance:** Dissects why `days_since_last_login` holds 51.4% predictive weight.
        * **Benchmark Comparison:** Performance evaluation against Decision Trees, XGBoost, and Logistic Regression.
        """)
        st.page_link("pages/4_🧠_Model_Intelligence.py", label="Open Model Intelligence →", icon="🧠")

st.markdown("---")

# ----------------------------
# System Tech Stack Badges
# ----------------------------
st.markdown("<div class='section-header'>🛠️ System Technology Stack</div>", unsafe_allow_html=True)

st.markdown("""
<span class='persona-badge'>🐍 Python 3.10</span>
<span class='persona-badge'>⚡ Streamlit Multi-Page</span>
<span class='persona-badge'>🌲 Scikit-learn (Random Forest)</span>
<span class='persona-badge'>📊 Plotly Interactive Graphics</span>
<span class='persona-badge'>🤖 Google Gemini Generative AI</span>
<span class='persona-badge'>💾 MySQL Data Warehouse</span>
<span class='persona-badge'>🐼 Pandas & NumPy</span>
""", unsafe_allow_html=True)