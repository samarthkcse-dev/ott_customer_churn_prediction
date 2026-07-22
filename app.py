import streamlit as st
import pandas as pd
import joblib

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
# Modify these dictionary values to match your dataset's original categories!
GENDER_MAP = {"Female":0,"Male":1,"Other":2,"Prefer not to say":3}
PLAN_MAP = {"Basic":0,"Premium":1,"Premium+":2,"Standard":3}
DEVICE_MAP = {"Mobile": 3, "Smart TV": 4, "Laptop": 2, "Tablet": 5,"Desktop":0,"Gaming Console":1}
AUTO_RENEW_MAP = {"No": 0, "Yes": 1}

# ----------------------------
# App Configuration
# ----------------------------
st.set_page_config(
    page_title="OTT Customer Churn Prediction",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 OTT Customer Churn Prediction")
st.markdown("### Predict whether a customer is likely to churn")

st.divider()

# ----------------------------
# Input Form
# ----------------------------
with st.form("churn_prediction_form"):
    st.subheader("Customer Details")
    
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        
        # Display readable text in selectboxes
        gender_selected = st.selectbox("Gender", list(GENDER_MAP.keys()))
        subscription_plan_selected = st.selectbox("Subscription Plan", list(PLAN_MAP.keys()))
        # monthly_charge = st.number_input("Monthly Charge", min_value=0.0, value=499.0)
        monthly_charge = st.selectbox(
        "Monthly Charge",
        options=[9.99, 15.99, 21.99, 29.99],
        index=0  # Defaults to 9.99
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
    # Convert string selections into numeric values using mapping dictionaries
    gender = GENDER_MAP[gender_selected]
    subscription_plan = PLAN_MAP[subscription_plan_selected]
    primary_device = DEVICE_MAP[primary_device_selected]
    auto_renew = AUTO_RENEW_MAP[auto_renew_selected]
    senior_user = 1 if senior_user_selected == "Yes" else 0

    # Build Feature DataFrame
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

    # Ensure feature order matches trained model
    input_df = input_df[features]

    # Inference
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]

    # Display Results
    st.divider()

    if prediction == 1:
        st.error("⚠️ Customer is likely to Churn")
    else:
        st.success("✅ Customer is likely to Stay")

    st.subheader("Prediction Probability")
    st.progress(float(probability[1]))

    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.metric("Stay Probability", f"{probability[0]*100:.2f}%")

    with res_col2:
        st.metric("Churn Probability", f"{probability[1]*100:.2f}%")