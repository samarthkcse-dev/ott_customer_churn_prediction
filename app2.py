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

# 1. Load environment variables
load_dotenv()

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="OTT Churn Predictor",
    page_icon="🎬",
    layout="wide"
)

inject_custom_css()

# ----------------------------
# Load Model & Files (Cached with Relative Paths)
# ----------------------------
try:
    model, features, encoders = load_model_assets()
except Exception as e:
    st.error(f"❌ Error loading model assets: {e}")
    st.stop()

# ----------------------------
# Header Section
# ----------------------------
st.markdown("<h1 class='hero-title'>🎬 OTT User Churn Predictor & Retention Copilot</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Predict churn risks, simulate retention strategies, and generate AI campaigns</p>", unsafe_allow_html=True)

# ----------------------------
# Instant Showcase Presets
# ----------------------------
st.markdown("<div class='section-header'>⚡ Quick Persona Presets (One-Click Showcase)</div>", unsafe_allow_html=True)

if "active_persona" not in st.session_state:
    st.session_state["active_persona"] = PERSONAS["🚨 At-Risk Dormant User"]

p_cols = st.columns(len(PERSONAS))
for idx, (p_name, p_data) in enumerate(PERSONAS.items()):
    with p_cols[idx]:
        if st.button(p_name, use_container_width=True):
            st.session_state["active_persona"] = p_data
            st.rerun()

curr = st.session_state["active_persona"]

# ----------------------------
# Input Form
# ----------------------------
st.markdown("<div class='section-header'>👤 Customer Profile & Activity</div>", unsafe_allow_html=True)

with st.form("churn_prediction_form"):
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown("#### 👤 Demographics")
        age = st.number_input("Age", min_value=18, max_value=100, value=int(curr.get("age", 30)))
        g_opts = list(GENDER_MAP.keys())
        g_idx = g_opts.index(curr.get("gender", "Male")) if curr.get("gender") in g_opts else 0
        gender_selected = st.selectbox("Gender", g_opts, index=g_idx)
        household_size = st.number_input("Household Size", min_value=1, max_value=10, value=int(curr.get("household_size", 3)))
        senior_user_selected = st.selectbox("Senior User (60+)", ["No", "Yes"], index=1 if curr.get("senior_user") == "Yes" else 0)

    with col2:
        st.markdown("#### 💳 Subscription & Billing")
        p_opts = list(PLAN_MAP.keys())
        p_idx = p_opts.index(curr.get("subscription_plan", "Standard")) if curr.get("subscription_plan") in p_opts else 0
        subscription_plan_selected = st.selectbox("Subscription Plan", p_opts, index=p_idx)
        
        charge_opts = [9.99, 15.99, 21.99, 29.99]
        curr_charge = float(curr.get("monthly_charge", 15.99))
        c_idx = charge_opts.index(curr_charge) if curr_charge in charge_opts else 1
        monthly_charge = st.selectbox("Monthly Charge ($)", options=charge_opts, index=c_idx)

        subscription_duration_days = st.number_input("Subscription Duration (Days)", min_value=1, value=int(curr.get("subscription_duration_days", 365)))
        ar_opts = list(AUTO_RENEW_MAP.keys())
        ar_idx = ar_opts.index(curr.get("auto_renew", "Yes")) if curr.get("auto_renew") in ar_opts else 1
        auto_renew_selected = st.selectbox("Auto Renew Enabled", ar_opts, index=ar_idx)
        payment_failures = st.number_input("Past Payment Failures", min_value=0, max_value=10, value=int(curr.get("payment_failures", 0)))

    with col3:
        st.markdown("#### 📺 Platform Activity")
        d_opts = list(DEVICE_MAP.keys())
        d_idx = d_opts.index(curr.get("primary_device", "Smart TV")) if curr.get("primary_device") in d_opts else 0
        primary_device_selected = st.selectbox("Primary Device", d_opts, index=d_idx)

        days_since_last_login = st.number_input("Days Since Last Login", min_value=0, max_value=180, value=int(curr.get("days_since_last_login", 5)))
        watch_hours = st.number_input("Watch Hours (Last 30 Days)", min_value=0.0, max_value=300.0, value=float(curr.get("watch_hours", 50.0)), step=1.0)

    st.write("")
    submit_button = st.form_submit_button("🔥 Predict Churn Status", use_container_width=True)

# ----------------------------
# Prediction Logic & Output
# ----------------------------
input_data = {
    "age": age,
    "gender": gender_selected,
    "subscription_plan": subscription_plan_selected,
    "monthly_charge": monthly_charge,
    "primary_device": primary_device_selected,
    "household_size": household_size,
    "subscription_duration_days": subscription_duration_days,
    "senior_user": senior_user_selected,
    "days_since_last_login": days_since_last_login,
    "auto_renew": auto_renew_selected,
    "payment_failures": payment_failures,
    "watch_hours": watch_hours
}

prediction, probability, encoded_df = predict_single(input_data, model, features)
churn_prob_pct = probability[1] * 100
stay_prob_pct = probability[0] * 100

st.markdown("<div class='section-header'>📊 Prediction Intelligence & Financial Impact</div>", unsafe_allow_html=True)

res_col1, res_col2 = st.columns([1.2, 1], gap="large")

with res_col1:
    fig_gauge = create_gauge_chart(churn_prob_pct)
    st.plotly_chart(fig_gauge, use_container_width=True)

with res_col2:
    if prediction == 1:
        st.error(f"🚨 **High Risk Alert:** Customer is predicted to **CHURN** ({churn_prob_pct:.1f}% risk). Immediate retention intervention advised.")
    else:
        st.success(f"🎉 **Customer Safe:** Customer is predicted to **STAY** ({stay_prob_pct:.1f}% retention probability).")

    m1, m2 = st.columns(2)
    with m1:
        st.metric("Stay Probability", f"{stay_prob_pct:.1f}%")
    with m2:
        st.metric("Churn Probability", f"{churn_prob_pct:.1f}%")

    m3, m4 = st.columns(2)
    with m3:
        st.metric("Monthly Revenue at Risk", f"${monthly_charge:.2f}/mo")
    with m4:
        st.metric("Annualized Value (ARR)", f"${monthly_charge * 12:.2f}/yr")

# ----------------------------
# Interactive "What-If" Sensitivity Simulator
# ----------------------------
st.markdown("<div class='section-header'>🎛️ Interactive 'What-If' Retention Simulator</div>", unsafe_allow_html=True)
st.caption("See how retention incentives alter customer churn probability dynamically:")

sim_col1, sim_col2, sim_col3 = st.columns(3)
with sim_col1:
    sim_auto = st.selectbox("Simulate Auto-Renew Status", ["Keep Current", "Turn Auto-Renew ON (Yes)"])
with sim_col2:
    sim_disc = st.selectbox("Simulate Pricing Offer", ["Current Price", "Apply 20% Discount", "Downgrade to Basic ($9.99)"])
with sim_col3:
    sim_hrs = st.slider("Simulate Additional Watch Hours (+hrs)", min_value=0, max_value=60, value=0, step=5)

sim_data = input_data.copy()
if "Turn" in sim_auto:
    sim_data["auto_renew"] = "Yes"
if "20%" in sim_disc:
    sim_data["monthly_charge"] = round(monthly_charge * 0.8, 2)
elif "Downgrade" in sim_disc:
    sim_data["monthly_charge"] = 9.99
    sim_data["subscription_plan"] = "Basic"
sim_data["watch_hours"] = min(300.0, watch_hours + sim_hrs)

sim_pred, sim_probs, _ = predict_single(sim_data, model, features)
sim_churn_pct = sim_probs[1] * 100
delta_pct = sim_churn_pct - churn_prob_pct

s1, s2 = st.columns([1, 2])
with s1:
    st.metric(
        label="Simulated Churn Risk",
        value=f"{sim_churn_pct:.1f}%",
        delta=f"{delta_pct:+.1f}%" if delta_pct != 0 else "0.0%",
        delta_color="inverse"
    )
with s2:
    if delta_pct < -5:
        st.info(f"💡 **Retention Impact:** This strategy reduces customer churn risk by **{abs(delta_pct):.1f}%**!")
    else:
        st.write("Adjust the simulation knobs above to explore effective retention strategies.")

# ----------------------------
# Gemini AI Retention Copilot
# ----------------------------
st.markdown("<div class='section-header'>💡 AI Retention Insights via Gemini</div>", unsafe_allow_html=True)

with st.spinner("Generating retention insights via Gemini..."):
    copilot_output = generate_retention_copilot(input_data, churn_prob_pct, prediction)
    st.markdown(f"<div class='ai-card'>{copilot_output}</div>", unsafe_allow_html=True)