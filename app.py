import streamlit as st
import pandas as pd
import joblib
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="OTT Customer Churn Prediction",
    page_icon="🎬",
    layout="centered"
)

# ----------------------------
# Load Model & Files
# ----------------------------
@st.cache_resource
def load_assets():
    base = os.path.dirname(os.path.abspath(__file__))
    model          = joblib.load(os.path.join(base, "models", "cust_churn_model.pkl"))
    label_encoders = joblib.load(os.path.join(base, "models", "encoder.pkl"))
    features       = joblib.load(os.path.join(base, "models", "features.pkl"))
    return model, label_encoders, features

model, label_encoders, features = load_assets()

# ----------------------------
# Mappings
# ----------------------------
GENDER_MAP    = {"Female": 0, "Male": 1, "Other": 2, "Prefer not to say": 3}
PLAN_MAP      = {"Basic": 0, "Premium": 1, "Premium+": 2, "Standard": 3}
DEVICE_MAP    = {"Mobile": 3, "Smart TV": 4, "Laptop": 2, "Tablet": 5, "Desktop": 0, "Gaming Console": 1}
AUTO_RENEW_MAP = {"No": 0, "Yes": 1}

# ----------------------------
# UI
# ----------------------------
st.title("🎬 OTT Customer Churn Prediction")
st.markdown("### Predict whether a customer is likely to churn")
st.divider()

with st.form("churn_form"):
    st.subheader("Customer Details")
    col1, col2 = st.columns(2)

    with col1:
        age                       = st.number_input("Age", min_value=18, max_value=100, value=30)
        gender_sel                = st.selectbox("Gender", list(GENDER_MAP.keys()))
        plan_sel                  = st.selectbox("Subscription Plan", list(PLAN_MAP.keys()))
        monthly_charge            = st.selectbox("Monthly Charge ($)", [9.99, 15.99, 21.99, 29.99])
        device_sel                = st.selectbox("Primary Device", list(DEVICE_MAP.keys()))
        household_size            = st.number_input("Household Size", min_value=1, max_value=10, value=3)

    with col2:
        subscription_duration_days = st.number_input("Subscription Duration (Days)", min_value=1, value=365)
        senior_user_sel            = st.selectbox("Senior User", ["No", "Yes"])
        days_since_last_login      = st.number_input("Days Since Last Login", min_value=0, value=5)
        auto_renew_sel             = st.selectbox("Auto Renew", list(AUTO_RENEW_MAP.keys()))
        payment_failures           = st.number_input("Payment Failures", min_value=0, value=0)
        watch_hours                = st.number_input("Watch Hours (Last 30 Days)", min_value=0.0, value=50.0)

    submitted = st.form_submit_button("🔍 Predict Churn", use_container_width=True)

# ----------------------------
# Prediction
# ----------------------------
if submitted:
    input_df = pd.DataFrame([{
        "age":                       age,
        "gender":                    GENDER_MAP[gender_sel],
        "subscription_plan":         PLAN_MAP[plan_sel],
        "Monthly_Charge":            monthly_charge,
        "primary_device":            DEVICE_MAP[device_sel],
        "household_size":            household_size,
        "subscription_duration_days": subscription_duration_days,
        "senior_user":               1 if senior_user_sel == "Yes" else 0,
        "days_since_last_login":     days_since_last_login,
        "auto_renew":                AUTO_RENEW_MAP[auto_renew_sel],
        "payment_failures":          payment_failures,
        "watch_hours_L30_days":      watch_hours,
    }])

    input_df    = input_df[features]
    prediction  = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]

    st.divider()

    if prediction == 1:
        st.error("⚠️ Customer is likely to **Churn**")
    else:
        st.success("✅ Customer is likely to **Stay**")

    st.subheader("Prediction Probability")
    st.progress(float(probability[1]))

    c1, c2 = st.columns(2)
    c1.metric("Stay Probability",  f"{probability[0]*100:.2f}%")
    c2.metric("Churn Probability", f"{probability[1]*100:.2f}%")

    # ----------------------------
    # Gemini AI Insights
    # ----------------------------
    st.divider()
    st.subheader("💡 AI Retention Insights (Gemini 3.6 Flash)")

    with st.spinner("Analysing customer profile..."):
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                st.warning("⚠️ GEMINI_API_KEY not found in .env — AI insights skipped.")
            else:
                client = genai.Client(api_key=api_key)
                prompt = f"""
You are an expert customer retention analyst for an OTT platform.
Analyse the following customer data and predicted churn status:

- Churn Probability      : {probability[1]*100:.1f}%
- Prediction             : {"Likely to Churn" if prediction == 1 else "Likely to Stay"}
- Subscription Plan      : {plan_sel} (${monthly_charge}/mo)
- Days Since Last Login  : {days_since_last_login} days
- Watch Hours (30 days)  : {watch_hours} hrs
- Payment Failures       : {payment_failures}
- Auto Renew             : {auto_renew_sel}
- Subscription Duration  : {subscription_duration_days} days
- Primary Device         : {device_sel}

Respond with clear bullet points:
1. **Primary Reasons** – Why is this customer at risk (or stable)?
2. **Actionable Recommendations** – 2-3 concrete strategies to retain this customer.
"""
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                )
                st.info(response.text)

        except Exception as e:
            st.error(f"❌ Could not generate AI insights: {e}")
