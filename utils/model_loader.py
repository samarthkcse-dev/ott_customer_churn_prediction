import os
from pathlib import Path
import joblib
import pandas as pd
import numpy as np
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
# Custom Mappings
# ----------------------------
GENDER_MAP = {"Female": 0, "Male": 1, "Other": 2, "Prefer not to say": 3}
PLAN_MAP = {"Basic": 0, "Premium": 1, "Premium+": 2, "Standard": 3}
DEVICE_MAP = {"Mobile": 3, "Smart TV": 4, "Laptop": 2, "Tablet": 5, "Desktop": 0, "Gaming Console": 1}
AUTO_RENEW_MAP = {"No": 0, "Yes": 1}

# Reverse maps for display
REV_GENDER_MAP = {v: k for k, v in GENDER_MAP.items()}
REV_PLAN_MAP = {v: k for k, v in PLAN_MAP.items()}
REV_DEVICE_MAP = {v: k for k, v in DEVICE_MAP.items()}
REV_AUTO_RENEW_MAP = {v: k for k, v in AUTO_RENEW_MAP.items()}

# ----------------------------
# Demo Personas for Instant Showcase
# ----------------------------
PERSONAS = {
    "🚨 At-Risk Dormant User": {
        "age": 32,
        "gender": "Male",
        "subscription_plan": "Basic",
        "monthly_charge": 9.99,
        "primary_device": "Mobile",
        "household_size": 1,
        "subscription_duration_days": 180,
        "senior_user": "No",
        "days_since_last_login": 42,
        "auto_renew": "No",
        "payment_failures": 2,
        "watch_hours": 4.5,
        "description": "Infrequent logins, cancelled auto-renew, past payment issues."
    },
    "💎 Loyal Premium Family": {
        "age": 42,
        "gender": "Female",
        "subscription_plan": "Premium+",
        "monthly_charge": 29.99,
        "primary_device": "Smart TV",
        "household_size": 4,
        "subscription_duration_days": 850,
        "senior_user": "No",
        "days_since_last_login": 2,
        "auto_renew": "Yes",
        "payment_failures": 0,
        "watch_hours": 85.0,
        "description": "High watch hours, long tenure, active auto-renew, family account."
    },
    "⚖️ Borderline At-Risk User": {
        "age": 28,
        "gender": "Other",
        "subscription_plan": "Standard",
        "monthly_charge": 15.99,
        "primary_device": "Laptop",
        "household_size": 2,
        "subscription_duration_days": 320,
        "senior_user": "No",
        "days_since_last_login": 21,
        "auto_renew": "Yes",
        "payment_failures": 1,
        "watch_hours": 22.0,
        "description": "Moderate watch time, recently reduced logins, standard tier."
    },
    "🎓 Price-Sensitive Student": {
        "age": 21,
        "gender": "Male",
        "subscription_plan": "Basic",
        "monthly_charge": 9.99,
        "primary_device": "Mobile",
        "household_size": 1,
        "subscription_duration_days": 90,
        "senior_user": "No",
        "days_since_last_login": 28,
        "auto_renew": "No",
        "payment_failures": 1,
        "watch_hours": 11.0,
        "description": "Budget plan, non-renewing, mobile only, at risk of cancellation."
    }
}

# ----------------------------
# Cached Asset Loaders
# ----------------------------
@st.cache_resource
def load_model_assets():
    """Loads the trained Random Forest model and features list using safe relative paths."""
    model_path = BASE_DIR / "models" / "cust_churn_model.pkl"
    features_path = BASE_DIR / "models" / "features.pkl"
    encoder_path = BASE_DIR / "models" / "encoder.pkl"

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}")
    if not features_path.exists():
        raise FileNotFoundError(f"Features file not found at {features_path}")

    model = joblib.load(model_path)
    features = joblib.load(features_path)
    encoders = joblib.load(encoder_path) if encoder_path.exists() else None

    return model, features, encoders

@st.cache_data
def load_dataset():
    """Loads the cleaned users dataset for dashboard analytics and batch demos."""
    data_path = BASE_DIR / "Data" / "Cleaned Data" / "users_cleaned_final.csv"
    if not data_path.exists():
        # Fallback to Data/users.csv if needed
        data_path = BASE_DIR / "Data" / "users.csv"
    if not data_path.exists():
        return None
    return pd.read_csv(data_path)

# ----------------------------
# Prediction Helpers
# ----------------------------
def predict_single(data_dict, model, features):
    """Encodes a single customer dictionary and returns prediction, probability array, and encoded df."""
    encoded_row = {
        "age": int(data_dict["age"]),
        "gender": GENDER_MAP.get(data_dict["gender"], 0),
        "subscription_plan": PLAN_MAP.get(data_dict["subscription_plan"], 0),
        "Monthly_Charge": float(data_dict["monthly_charge"]),
        "primary_device": DEVICE_MAP.get(data_dict["primary_device"], 0),
        "household_size": int(data_dict["household_size"]),
        "subscription_duration_days": int(data_dict["subscription_duration_days"]),
        "senior_user": 1 if data_dict["senior_user"] in [1, "Yes", "1"] else 0,
        "days_since_last_login": int(data_dict["days_since_last_login"]),
        "auto_renew": AUTO_RENEW_MAP.get(data_dict["auto_renew"], 0) if isinstance(data_dict["auto_renew"], str) else int(data_dict["auto_renew"]),
        "payment_failures": int(data_dict["payment_failures"]),
        "watch_hours_L30_days": float(data_dict["watch_hours"])
    }

    df = pd.DataFrame([encoded_row])[features]
    prediction = int(model.predict(df)[0])
    probabilities = model.predict_proba(df)[0]
    return prediction, probabilities, df

def predict_batch(input_df, model, features):
    """
    Safely encodes and predicts on a batch DataFrame.
    Returns a copy of the dataframe with added predictions and risk categories.
    """
    df = input_df.copy()
    
    # Handle possible column name casing variations
    col_mapping = {
        "monthly_charge": "Monthly_Charge",
        "watch_hours": "watch_hours_L30_days",
        "watch_hours_l30_days": "watch_hours_L30_days"
    }
    for old_col, new_col in col_mapping.items():
        if old_col in df.columns and new_col not in df.columns:
            df.rename(columns={old_col: new_col}, inplace=True)

    df_encoded = df.copy()

    # Map categorical columns if strings
    if df_encoded["gender"].dtype == "object":
        df_encoded["gender"] = df_encoded["gender"].map(GENDER_MAP).fillna(0)
    if df_encoded["subscription_plan"].dtype == "object":
        df_encoded["subscription_plan"] = df_encoded["subscription_plan"].map(PLAN_MAP).fillna(0)
    if df_encoded["primary_device"].dtype == "object":
        df_encoded["primary_device"] = df_encoded["primary_device"].map(DEVICE_MAP).fillna(0)
    if df_encoded["auto_renew"].dtype == "object":
        df_encoded["auto_renew"] = df_encoded["auto_renew"].map(AUTO_RENEW_MAP).fillna(0)
    if "senior_user" in df_encoded.columns and df_encoded["senior_user"].dtype == "object":
        df_encoded["senior_user"] = df_encoded["senior_user"].apply(lambda x: 1 if str(x).strip().lower() in ["yes", "1"] else 0)

    X = df_encoded[features]
    preds = model.predict(X)
    probs = model.predict_proba(X)[:, 1]

    df["Predicted_Churn"] = preds
    df["Churn_Probability"] = np.round(probs * 100, 2)
    df["Risk_Level"] = pd.cut(
        df["Churn_Probability"],
        bins=[-0.1, 35, 65, 100.1],
        labels=["Low Risk (Safe)", "Moderate Risk", "High Risk (Critical)"]
    )
    return df
