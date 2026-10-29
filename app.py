import streamlit as st
import pandas as pd
import joblib
from google import genai
import os
from dotenv import load_dotenv

# 1. Load environment variables at app start
load_dotenv()

# ----------------------------
# App Configuration & Blue-Pink Theme Styling
# ----------------------------
st.set_page_config(
    page_title="OTT Customer Churn Prediction",
    page_icon="🎬",
    layout="centered"
)

# Custom CSS for Blue-Pink Theme
st.markdown("""
    <style>
    /* Main background & font style */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Title styling */
    h1 {
        color: #ff1493 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    h3 {
        color: #1e3a8a !important;
    }

    /* Form container background */
    [data-testid="stForm"] {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255, 20, 147, 0.15);
        border: 1px solid rgba(255, 20, 147, 0.2);
    }

    /* Primary Submit Button styling (Pink-Blue gradient) */
    .stFormSubmitButton button {
        background: linear-gradient(90deg, #ff1493 0%, #3b82f6 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1rem;
        transition: 0.3s ease;
    }
    
    .stFormSubmitButton button:hover {
        opacity: 0.9;
        box-shadow: 0 4px 10px rgba(255, 20, 147, 0.3);
    }

    /* Metric cards styling */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(30, 58, 138, 0.1);
        border-left: 4px solid #ff1493;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Load Model & Files (Cached for Performance)
# ----------------------------
@st.cache_resource
def load_assets():
    model = joblib.load("C:/Users/samar/Desktop/samarth15/OTT platform customer churn prediction/models/cust_churn_model.pkl")
    label_encoders = joblib.load("C:/Users/samar/Desktop/samarth15/OTT platform customer churn prediction/models/encoder.pkl")
    features = joblib.load("C:/Users/samar/Desktop/samarth15/OTT platform customer churn prediction/models/features.pkl")
    return model, label_encoders, features

model, label_encoders, features = load_assets()

# ----------------------------
# Custom Mappings (Map text labels to numeric values)
# ----------------------------
GENDER_MAP = {"Female":0,"Male":1,"Other":2,"Prefer not to say":3}
PLAN_MAP = {"Basic":0,"Premium":1,"Premium+":2,"Standard":3}
DEVICE_MAP = {"Mobile": 3, "Smart TV": 4, "Laptop": 2, "Tablet": 5,"Desktop":0,"Gaming Console":1}
AUTO_RENEW_MAP = {"No": 0, "Yes": 1}

st.title("🎬 OTT Customer Churn Prediction")
st.markdown("### Predict whether a customer is likely to churn[cite: 1]")

st.divider()

# ----------------------------
# Input Form
# ----------------------------
with st.form("churn_prediction_form"):
    st.subheader("Customer Details[cite: 1]")
    
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        gender_selected = st.selectbox("Gender", list(GENDER_MAP.keys()))
        subscription_plan_selected = st.selectbox("Subscription Plan", list(PLAN_MAP.keys()))
        monthly_charge = st.selectbox(
            "Monthly Charge",
            options=[9.99, 15.99, 21.99, 29.99],
            index=0
        )
        primary_device_selected = st.selectbox("Primary Device", list(DEVICE_MAP.keys()))
        household_size = st.number_input("Household Size", min_value=1, max_value=10, value=3)

    with col2:
        subscription_duration_days = st.number_input("Subscription Duration (Days)", min_value=1, value=365)
        senior_user_selected = st.selectbox("Senior User", ["No", "Yes"])
        days_since_last_login = st.number_input("Days Since Last Login", min_value=0, value=5)
        auto_renew_selected = st.selectbox("Auto Renew", list(AUTO_RENEW_MAP.keys()))
        payment_failures = st.number_input("Payment Failures", min_value=0, value=0)
        watch_hours = st.number_input("Watch Hours (Last 30 Days)", min_value=0.0, value=50.0)

    # Form Submit Button
    submit_button = st.form_submit_button("Predict Churn", use_container_width=True)

# ----------------------------
# Prediction Logic
# ----------------------------
if submit_button:
    gender = GENDER_MAP[gender_selected]
    subscription_plan = PLAN_PLAN = PLAN_MAP[subscription_plan_selected]
    primary_device = DEVICE_MAP[primary_device_selected]
    auto_renew = AUTO_RENEW_MAP[auto_renew_selected]
    senior_user = 1 if senior_user_selected == "Yes" else 0

    input_df = pd.DataFrame([{
        "age": age,
        "gender": gender,
        "subscription_plan": subscription_plan,
        "Monthly_Charge": monthly_charge,
        "primary_device": primary_device,
        "household_size": household_size,
        "subscription_duration_days": subscription_duration_days,
        "senior_user": senior_user,
        "days_since_last_login": days_since_last_login,
        "auto_renew": auto_renew,
        "payment_failures": payment_failures,
        "watch_hours_L30_days": watch_hours
    }])

    input_df = input_df[features]

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]

    st.divider()

    if prediction == 1:
        st.error("⚠️ Customer is likely to Churn")
    else:
        st.success("✅ Customer is likely to Stay")

    st.subheader("Prediction Probability[cite: 1]")
    st.progress(float(probability[1]))

    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.metric("Stay Probability", f"{probability[0]*100:.2f}%")

    with res_col2:
        st.metric("Churn Probability", f"{probability[1]*100:.2f}%")

    # ----------------------------
    # Gemini AI Insights Integration
    # ----------------------------
    st.divider()
    st.subheader("💡 AI Retention Insights (Powered by Gemini 2.5 Flash)[cite: 1]")

    with st.spinner("Analyzing customer profile...[cite: 1]"):
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            
            if not api_key:
                st.error("❌ API Key missing! Make sure GEMINI_API_KEY is defined in your .env file.[cite: 1]")
            else:
                client = genai.Client(api_key=api_key)

                prompt = f"""
                You are an expert customer retention analyst for an OTT platform. 
                Analyze the following customer metrics and predicted churn status:

                - Predicted Churn Probability: {probability[1]*100:.1f}%
                - Prediction Result: {"Likely to Churn" if prediction == 1 else "Likely to Stay"}
                - Subscription Plan: {subscription_plan_selected} (${monthly_charge}/mo)
                - Days Since Last Login: {days_since_last_login} days
                - Watch Hours (Last 30 Days): {watch_hours} hours
                - Payment Failures: {payment_failures}
                - Auto Renew: {auto_renew_selected}
                - Subscription Duration: {subscription_duration_days} days
                - Primary Device: {primary_device_selected}

                Provide a brief response using very simple and clear bullet points:
                1. **Primary Reasons**: High-level explanation of why this customer is at risk (or why they are stable).
                2. **Actionable Recommendations**: 2 to 3 simple strategies or offers to retain this specific customer.
                """

                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                )

                st.info(response.text)

        except Exception as e:
            st.error(f"❌ Could not generate AI insights: {e}")