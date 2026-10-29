import streamlit as st
import pandas as pd
import joblib
from google import genai
import os
from dotenv import load_dotenv

# 1. Load environment variables at app start
load_dotenv()

# ----------------------------
# App Configuration & Page Layout
# ----------------------------
st.set_page_config(
    page_title="OTT Churn Predictor",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for Professional Blue & Pink UI
st.markdown("""
<style>
    /* Clean Professional Dark Blue Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0b132b, #1c2541, #243b55);
        color: #ffffff;
    }

    /* Gradient Header (Professional Blue to Pink) */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #ff3366, #ff6b6b, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .sub-header {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Container Box Styling */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }

    /* Section Subheadings */
    .section-title {
        color: #4facfe;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #4facfe;
        padding-bottom: 5px;
        display: inline-block;
    }

    /* Custom Form Submit Button (Pink to Blue Professional Gradient) */
    div.stButton > button {
        background: linear-gradient(90deg, #ff3366, #ff5e62);
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 4px 15px rgba(255, 51, 102, 0.3);
        transition: all 0.3s ease-in-out;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 51, 102, 0.5);
        background: linear-gradient(90deg, #ff5e62, #ff3366);
    }

    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
    }

    /* AI Card Container */
    .ai-card {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1), rgba(255, 51, 102, 0.1));
        border: 1px solid rgba(79, 172, 254, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Load Model & Files (Cached)
# ----------------------------
@st.cache_resource
def load_assets():
    model = joblib.load("C:/Users/samar/Desktop/samarth15/OTT platform customer churn prediction/models/cust_churn_model.pkl")
    label_encoders = joblib.load("C:/Users/samar/Desktop/samarth15/OTT platform customer churn prediction/models/encoder.pkl")
    features = joblib.load("C:/Users/samar/Desktop/samarth15/OTT platform customer churn prediction/models/features.pkl")
    return model, label_encoders, features

model, label_encoders, features = load_assets()

# ----------------------------
# Custom Mappings
# ----------------------------
GENDER_MAP = {"Female": 0, "Male": 1, "Other": 2, "Prefer not to say": 3}
PLAN_MAP = {"Basic": 0, "Premium": 1, "Premium+": 2, "Standard": 3}
DEVICE_MAP = {"Mobile": 3, "Smart TV": 4, "Laptop": 2, "Tablet": 5, "Desktop": 0, "Gaming Console": 1}
AUTO_RENEW_MAP = {"No": 0, "Yes": 1}

# ----------------------------
# Header Section
# ----------------------------
st.markdown("<h1 class='main-header'>🎬 OTT User Churn Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Predict churn risks and generate retention strategies using AI</p>", unsafe_allow_html=True)

# ----------------------------
# Input Form
# ----------------------------
with st.form("churn_prediction_form"):
    st.markdown("<div class='section-title'>👤 Customer Profile & Activity</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")

    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        gender_selected = st.selectbox("Gender", list(GENDER_MAP.keys()))
        subscription_plan_selected = st.selectbox("Subscription Plan", list(PLAN_MAP.keys()))
        monthly_charge = st.selectbox(
            "Monthly Charge ($)",
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

    st.write("")
    submit_button = st.form_submit_button("🔥 Predict Churn Status", use_container_width=True)

# ----------------------------
# Prediction Logic & Output
# ----------------------------
if submit_button:
    gender = GENDER_MAP[gender_selected]
    subscription_plan = PLAN_MAP[subscription_plan_selected]
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

    st.markdown("---")
    st.markdown("<div class='section-title'>📊 Prediction Results</div>", unsafe_allow_html=True)

    if prediction == 1:
        st.error("🚨 **High Risk Alert:** Customer is likely to **Churn**")
    else:
        st.success("🎉 **Safe:** Customer is likely to **Stay**")

    st.progress(float(probability[1]))

    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric("Stay Probability", f"{probability[0]*100:.2f}%")
    with res_col2:
        st.metric("Churn Probability", f"{probability[1]*100:.2f}%")

    # ----------------------------
    # Gemini AI Insights
    # ----------------------------
    st.markdown("<div class='section-title' style='margin-top: 2rem;'>💡 AI Retention Insights</div>", unsafe_allow_html=True)

    with st.spinner("Generating retention insights via Gemini..."):
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            
            if not api_key:
                st.error("❌ API Key missing! Check your .env file for GEMINI_API_KEY.")
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

                Provide a brief response using simple bullet points:
                1. **Primary Reasons**: High-level explanation of risk/stability.
                2. **Actionable Recommendations**: 2 to 3 simple strategies or offers to retain this customer.
                """

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt,
                )

                st.markdown(f"<div class='ai-card'>{response.text}</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Could not generate AI insights: {e}")
            #final