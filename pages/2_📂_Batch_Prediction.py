import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

from utils.model_loader import load_model_assets, load_dataset, predict_batch
from utils.ui_components import inject_custom_css

load_dotenv()

st.set_page_config(
    page_title="Batch Churn Intelligence | OTT Platform",
    page_icon="📂",
    layout="wide"
)

inject_custom_css()

# Load Model
try:
    model, features, encoders = load_model_assets()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.markdown("<h1 class='hero-title'>📂 Batch Churn Prediction & Portfolio Risk</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Upload customer cohorts or evaluate active subscriber portfolios for churn exposure</p>", unsafe_allow_html=True)

# ----------------------------
# Input Options: Upload or Sample
# ----------------------------
st.markdown("<div class='section-header'>📥 Data Ingestion</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    uploaded_file = st.file_uploader("Upload Customer CSV file", type=["csv"], help="CSV must contain subscriber profile and usage columns.")

with col2:
    st.markdown("#### Or test instantly:")
    load_sample = st.button("⚡ Load 150 Sample Customers from Database", use_container_width=True)

df_to_predict = None

if uploaded_file is not None:
    try:
        df_to_predict = pd.read_csv(uploaded_file)
        st.success(f"Successfully loaded {len(df_to_predict)} records from uploaded CSV.")
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")
elif load_sample or ("batch_df" in st.session_state):
    full_df = load_dataset()
    if full_df is not None:
        if "batch_df" not in st.session_state or load_sample:
            # Sample 150 random records with fixed seed for reproducibility
            st.session_state["batch_df"] = full_df.sample(n=min(150, len(full_df)), random_state=42).copy()
        df_to_predict = st.session_state["batch_df"]
        st.info(f"Loaded {len(df_to_predict)} real subscriber records from OTT platform dataset.")
    else:
        st.warning("Sample dataset not found.")

if df_to_predict is not None:
    # ----------------------------
    # Run Batch Prediction
    # ----------------------------
    with st.spinner("Executing Random Forest predictions across cohort..."):
        try:
            results_df = predict_batch(df_to_predict, model, features)
        except Exception as e:
            st.error(f"Prediction failed. Ensure CSV contains expected features. Error: {e}")
            st.stop()

    total_customers = len(results_df)
    churn_count = int(results_df["Predicted_Churn"].sum())
    churn_rate = (churn_count / total_customers) * 100
    
    # Revenue at risk calculation
    charge_col = "Monthly_Charge" if "Monthly_Charge" in results_df.columns else "monthly_charge"
    if charge_col in results_df.columns:
        mrr_at_risk = results_df[results_df["Predicted_Churn"] == 1][charge_col].sum()
    else:
        mrr_at_risk = churn_count * 16.99  # estimated average
    
    avg_churn_prob = results_df["Churn_Probability"].mean()

    # ----------------------------
    # Portfolio KPIs
    # ----------------------------
    st.markdown("<div class='section-header'>📈 Portfolio Risk Overview</div>", unsafe_allow_html=True)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("Total Cohort Analyzed", f"{total_customers:,}")
    with kpi2:
        st.metric("Subscribers at Risk", f"{churn_count:,} ({churn_rate:.1f}%)")
    with kpi3:
        st.metric("Monthly Revenue at Risk", f"${mrr_at_risk:,.2f}")
    with kpi4:
        st.metric("Avg Cohort Churn Prob", f"{avg_churn_prob:.1f}%")

    # ----------------------------
    # Visual Analytics
    # ----------------------------
    st.markdown("<div class='section-header'>📊 Risk Segmentation Breakdown</div>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        risk_counts = results_df["Risk_Level"].value_counts().reset_index()
        risk_counts.columns = ["Risk_Level", "Count"]
        
        color_map = {
            "Low Risk (Safe)": "#10b981",
            "Moderate Risk": "#f59e0b",
            "High Risk (Critical)": "#ff3366"
        }

        fig_donut = px.pie(
            risk_counts,
            names="Risk_Level",
            values="Count",
            hole=0.55,
            color="Risk_Level",
            color_discrete_map=color_map,
            title="<b>Cohort Risk Distribution</b>"
        )
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#f8fafc'},
            legend=dict(orientation="h", y=-0.1)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with chart_col2:
        plan_col = "subscription_plan" if "subscription_plan" in results_df.columns else None
        if plan_col:
            plan_churn = results_df.groupby([plan_col, "Risk_Level"], observed=False).size().reset_index(name="Count")
            fig_bar = px.bar(
                plan_churn,
                x=plan_col,
                y="Count",
                color="Risk_Level",
                color_discrete_map=color_map,
                barmode="stack",
                title="<b>Risk Segmentation by Subscription Tier</b>"
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#f8fafc'},
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
                legend=dict(orientation="h", y=-0.2)
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    # ----------------------------
    # Detailed Data Table & Export
    # ----------------------------
    st.markdown("<div class='section-header'>📋 Enriched Customer Records</div>", unsafe_allow_html=True)

    # Select key display columns
    display_cols = [
        c for c in [
            "user_id", "email", "first_name", "subscription_plan", "Monthly_Charge",
            "primary_device", "days_since_last_login", "watch_hours_L30_days",
            "Churn_Probability", "Risk_Level", "Predicted_Churn"
        ] if c in results_df.columns
    ]

    # Filters
    f1, f2 = st.columns([1, 2])
    with f1:
        filter_risk = st.multiselect("Filter by Risk Level", options=results_df["Risk_Level"].unique(), default=results_df["Risk_Level"].unique())
    
    filtered_results = results_df[results_df["Risk_Level"].isin(filter_risk)]

    st.dataframe(filtered_results[display_cols] if display_cols else filtered_results, use_container_width=True, height=350)

    # Download Button
    csv_bytes = results_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Full Scored Portfolio CSV",
        data=csv_bytes,
        file_name="ott_churn_scored_portfolio.csv",
        mime="text/csv",
        use_container_width=True
    )
else:
    st.info("👆 Upload a customer CSV file or click 'Load 150 Sample Customers' to begin cohort analysis.")
