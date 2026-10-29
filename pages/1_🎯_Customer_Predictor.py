import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv

from utils.model_loader import (
    load_model_assets,
    predict_single,
    PERSONAS,
    GENDER_MAP,
    PLAN_MAP,
    DEVICE_MAP,
    AUTO_RENEW_MAP
)
from utils.ui_components import (
    inject_custom_css,
    create_gauge_chart,
    generate_retention_copilot
)

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Single Customer Predictor | OTT Churn Intelligence",
    page_icon="🎯",
    layout="wide"
)

inject_custom_css()

# Load Model Assets
try:
    model, features, encoders = load_model_assets()
except Exception as e:
    st.error(f"Error loading model assets: {e}")
    st.stop()

# ----------------------------
# Header
# ----------------------------
st.markdown("<h1 class='hero-title'>🎯 Real-Time Customer Churn Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Evaluate individual subscriber attrition probability and trigger AI retention actions</p>", unsafe_allow_html=True)

# ----------------------------
# Quick-Load Persona Presets
# ----------------------------
st.markdown("<div class='section-header'>⚡ Instant Showcase Presets (One-Click Demo)</div>", unsafe_allow_html=True)
st.caption("Click any persona below to instantly populate the form with realistic user profiles:")

# Session state initialization for form inputs
if "current_profile" not in st.session_state:
    st.session_state["current_profile"] = PERSONAS["🚨 At-Risk Dormant User"]

p_cols = st.columns(len(PERSONAS))
for idx, (p_name, p_data) in enumerate(PERSONAS.items()):
    with p_cols[idx]:
        if st.button(p_name, use_container_width=True):
            st.session_state["current_profile"] = p_data
            st.rerun()

curr = st.session_state["current_profile"]

# ----------------------------
# Customer Input Form
# ----------------------------
st.markdown("<div class='section-header'>👤 Customer Profile & Activity Parameters</div>", unsafe_allow_html=True)

with st.form("single_prediction_form"):
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("#### 👤 Demographics")
        age = st.number_input("Age", min_value=18, max_value=100, value=int(curr.get("age", 30)))
        gender_options = list(GENDER_MAP.keys())
        gender_index = gender_options.index(curr.get("gender", "Male")) if curr.get("gender") in gender_options else 0
        gender = st.selectbox("Gender", gender_options, index=gender_index)
        
        household_size = st.number_input("Household Size", min_value=1, max_value=10, value=int(curr.get("household_size", 2)))
        senior_user = st.selectbox("Senior User (60+)", ["No", "Yes"], index=1 if curr.get("senior_user") == "Yes" else 0)

    with col2:
        st.markdown("#### 💳 Subscription & Billing")
        plan_options = list(PLAN_MAP.keys())
        plan_index = plan_options.index(curr.get("subscription_plan", "Standard")) if curr.get("subscription_plan") in plan_options else 0
        subscription_plan = st.selectbox("Subscription Plan", plan_options, index=plan_index)
        
        monthly_charge_opts = [9.99, 15.99, 21.99, 29.99]
        curr_charge = float(curr.get("monthly_charge", 15.99))
        charge_index = monthly_charge_opts.index(curr_charge) if curr_charge in monthly_charge_opts else 1
        monthly_charge = st.selectbox("Monthly Charge ($)", options=monthly_charge_opts, index=charge_index)

        duration_days = st.number_input("Subscription Tenure (Days)", min_value=1, value=int(curr.get("subscription_duration_days", 365)))
        auto_renew = st.selectbox("Auto Renew Enabled", list(AUTO_RENEW_MAP.keys()), index=0 if curr.get("auto_renew") == "No" else 1)
        payment_failures = st.number_input("Past Payment Failures", min_value=0, max_value=10, value=int(curr.get("payment_failures", 0)))

    with col3:
        st.markdown("#### 📱 Platform Engagement")
        device_options = list(DEVICE_MAP.keys())
        device_index = device_options.index(curr.get("primary_device", "Smart TV")) if curr.get("primary_device") in device_options else 0
        primary_device = st.selectbox("Primary Streaming Device", device_options, index=device_index)

        days_since_last_login = st.number_input("Days Since Last Login", min_value=0, max_value=180, value=int(curr.get("days_since_last_login", 5)))
        watch_hours = st.number_input("Watch Hours (Last 30 Days)", min_value=0.0, max_value=300.0, value=float(curr.get("watch_hours", 40.0)), step=1.0)

    st.write("")
    predict_clicked = st.form_submit_button("🔥 Compute Churn Prediction", use_container_width=True)

# ----------------------------
# Execution & Prediction Results
# ----------------------------
# We also compute whenever page loads so the demo starts immediately with the selected persona
input_data = {
    "age": age,
    "gender": gender,
    "subscription_plan": subscription_plan,
    "monthly_charge": monthly_charge,
    "primary_device": primary_device,
    "household_size": household_size,
    "subscription_duration_days": duration_days,
    "senior_user": senior_user,
    "days_since_last_login": days_since_last_login,
    "auto_renew": auto_renew,
    "payment_failures": payment_failures,
    "watch_hours": watch_hours
}

prediction, probabilities, encoded_df = predict_single(input_data, model, features)
churn_prob_pct = probabilities[1] * 100
stay_prob_pct = probabilities[0] * 100

st.markdown("<div class='section-header'>📊 Prediction Intelligence & Financial Impact</div>", unsafe_allow_html=True)

res_col1, res_col2 = st.columns([1.2, 1], gap="large")

with res_col1:
    fig_gauge = create_gauge_chart(churn_prob_pct)
    st.plotly_chart(fig_gauge, use_container_width=True)

with res_col2:
    if prediction == 1:
        st.error(f"🚨 **High Risk Alert:** Customer is predicted to **CHURN** ({churn_prob_pct:.1f}% risk). Immediate retention intervention advised.")
    else:
        st.success(f"🎉 **Customer Stable:** Customer is predicted to **STAY** ({stay_prob_pct:.1f}% retention probability).")

    # Financial Exposure Cards
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Monthly Revenue at Risk", f"${monthly_charge:.2f}/mo")
    with m2:
        annual_risk = monthly_charge * 12
        st.metric("Annualized Value (ARR)", f"${annual_risk:.2f}/yr")

    m3, m4 = st.columns(2)
    with m3:
        st.metric("Tenure Length", f"{duration_days} days")
    with m4:
        clv_tier = "High CLV" if monthly_charge >= 21.99 and duration_days > 365 else ("Mid CLV" if duration_days > 180 else "Growth Tier")
        st.metric("Account Tier", clv_tier)

# ----------------------------
# Interactive "What-If" Sensitivity Simulator
# ----------------------------
st.markdown("<div class='section-header'>🎛️ Interactive 'What-If' Retention Simulator</div>", unsafe_allow_html=True)
st.caption("Test how targeted retention interventions dynamically influence churn risk in real-time:")

sim_col1, sim_col2, sim_col3 = st.columns(3)
with sim_col1:
    sim_auto_renew = st.selectbox("Simulate Auto-Renew Status", ["Keep Current", "Force Enable Auto-Renew (Yes)"])
with sim_col2:
    sim_discount = st.selectbox("Simulate Price Discount", ["No Discount", "Offer 20% Discount", "Downgrade to Basic ($9.99)"])
with sim_col3:
    sim_engagement = st.slider("Simulate Extra Watch Hours (+hrs)", min_value=0, max_value=60, value=0, step=5)

# Calculate simulated probability
sim_data = input_data.copy()
if "Force" in sim_auto_renew:
    sim_data["auto_renew"] = "Yes"
if "20%" in sim_discount:
    sim_data["monthly_charge"] = round(monthly_charge * 0.8, 2)
elif "Downgrade" in sim_discount:
    sim_data["monthly_charge"] = 9.99
    sim_data["subscription_plan"] = "Basic"
sim_data["watch_hours"] = min(300.0, watch_hours + sim_engagement)

sim_pred, sim_probs, _ = predict_single(sim_data, model, features)
sim_churn_pct = sim_probs[1] * 100
delta_pct = sim_churn_pct - churn_prob_pct

s_col1, s_col2 = st.columns([1, 2])
with s_col1:
    st.metric(
        label="Simulated Churn Probability",
        value=f"{sim_churn_pct:.1f}%",
        delta=f"{delta_pct:+.1f}% Risk Reduction" if delta_pct <= 0 else f"{delta_pct:+.1f}% Risk Increase",
        delta_color="inverse"
    )
with s_col2:
    if delta_pct < -5:
        st.info(f"💡 **Strategy Impact:** This retention intervention lowers customer churn probability by **{abs(delta_pct):.1f}%**!")
    else:
        st.write("Adjust the controls above to test hypothetical offers and engagement campaigns.")

# ----------------------------
# Gemini AI Retention Copilot
# ----------------------------
st.markdown("<div class='section-header'>🤖 Gemini AI Retention Strategist</div>", unsafe_allow_html=True)

with st.spinner("Synthesizing tailored retention intelligence..."):
    copilot_output = generate_retention_copilot(input_data, churn_prob_pct, prediction)
    st.markdown(f"<div class='ai-card'>{copilot_output}</div>", unsafe_allow_html=True)
