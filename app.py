import streamlit as st
import pandas as pd
import joblib

# ----------------------------
# Load Model & Files
# ----------------------------
model = joblib.load("C:/Users/samar/Desktop/samarth15/OTT platform customer churn prediction/models/cust_churn_model.pkl")
label_encoders = joblib.load("C:/Users/samar/Desktop/samarth15/OTT platform customer churn prediction/models/label_encoders.pkl")
features = joblib.load("C:/Users/samar/Desktop/samarth15/OTT platform customer churn prediction/models/features.pkl")

st.set_page_config(
    page_title="OTT Customer Churn Prediction",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 OTT Customer Churn Prediction")
st.markdown("### Predict whether a customer is likely to churn")

st.divider()

# ----------------------------
# User Inputs
# ----------------------------

age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=30
)

gender = st.selectbox(
    "Gender",
    label_encoders["gender"].classes_
)

subscription_plan = st.selectbox(
    "Subscription Plan",
    label_encoders["subscription_plan"].classes_
)

monthly_charge = st.number_input(
    "Monthly Charge",
    min_value=0.0,
    value=499.0
)

primary_device = st.selectbox(
    "Primary Device",
    label_encoders["primary_device"].classes_
)

household_size = st.number_input(
    "Household Size",
    min_value=1,
    max_value=10,
    value=3
)

subscription_duration_days = st.number_input(
    "Subscription Duration (Days)",
    min_value=1,
    value=365
)

senior_user = st.selectbox(
    "Senior User",
    [0,1]
)

days_since_last_login = st.number_input(
    "Days Since Last Login",
    min_value=0,
    value=5
)

auto_renew = st.selectbox(
    "Auto Renew",
    label_encoders["auto_renew"].classes_
)

payment_failures = st.number_input(
    "Payment Failures",
    min_value=0,
    value=0
)

watch_hours = st.number_input(
    "Watch Hours (Last 30 Days)",
    min_value=0.0,
    value=50.0
)

# ----------------------------
# Prediction
# ----------------------------

if st.button("Predict Churn", use_container_width=True):

    gender = label_encoders["gender"].transform([gender])[0]

    subscription_plan = label_encoders["subscription_plan"].transform(
        [subscription_plan]
    )[0]

    primary_device = label_encoders["primary_device"].transform(
        [primary_device]
    )[0]

    auto_renew = label_encoders["auto_renew"].transform(
        [auto_renew]
    )[0]

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

    # Ensure feature order matches training
    input_df = input_df[features]

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0]

    st.divider()

    if prediction == 1:
        st.error("⚠️ Customer is likely to Churn")
    else:
        st.success("✅ Customer is likely to Stay")

    st.subheader("Prediction Probability")

    st.progress(float(probability[1]))

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Stay",
            f"{probability[0]*100:.2f}%"
        )

    with col2:
        st.metric(
            "Churn",
            f"{probability[1]*100:.2f}%"
        )