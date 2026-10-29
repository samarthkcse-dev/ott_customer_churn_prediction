import os
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from google import genai

# ----------------------------
# Global CSS Injector
# ----------------------------
def inject_custom_css():
    """Injects high-end, responsive dark theme styling across all pages."""
    st.markdown("""
    <style>
        /* Base Dark Modern Theme */
        .stApp {
            background: linear-gradient(135deg, #090e1f 0%, #111b33 50%, #172647 100%);
            color: #f8fafc;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        /* Gradient Hero Headers */
        .hero-title {
            font-size: 2.6rem;
            font-weight: 800;
            text-align: center;
            background: -webkit-linear-gradient(45deg, #ff3366, #ff6b6b, #4facfe, #00f2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.3rem;
        }
        
        .hero-subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 1.15rem;
            margin-bottom: 2rem;
            font-weight: 400;
        }

        /* Section Subheadings */
        .section-header {
            color: #4facfe;
            font-size: 1.35rem;
            font-weight: 600;
            margin: 1.5rem 0 1rem 0;
            padding-bottom: 6px;
            border-bottom: 2px solid rgba(79, 172, 254, 0.4);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Glassmorphism Containers */
        div[data-testid="stForm"], div.glass-card {
            background: rgba(255, 255, 255, 0.035);
            border-radius: 16px;
            padding: 1.75rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(12px);
        }

        /* Metric Cards */
        div[data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.04);
            padding: 1.1rem;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            text-align: center;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }
        div[data-testid="stMetric"] label {
            color: #94a3b8 !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: #f8fafc !important;
        }

        /* Custom Primary Action Buttons */
        div.stButton > button[kind="primary"], .submit-btn button {
            background: linear-gradient(90deg, #ff3366 0%, #ff5e62 100%) !important;
            color: white !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            border: none !important;
            padding: 0.65rem 1.8rem !important;
            box-shadow: 0 4px 15px rgba(255, 51, 102, 0.35) !important;
            transition: all 0.25s ease-in-out !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 51, 102, 0.5) !important;
        }

        /* AI Retention Card */
        .ai-card {
            background: linear-gradient(135deg, rgba(79, 172, 254, 0.08), rgba(255, 51, 102, 0.08));
            border: 1px solid rgba(79, 172, 254, 0.3);
            border-radius: 14px;
            padding: 1.5rem;
            margin-top: 1.2rem;
            line-height: 1.6;
        }

        /* Persona Pill Badges */
        .persona-badge {
            display: inline-block;
            background: rgba(79, 172, 254, 0.15);
            color: #4facfe;
            border: 1px solid rgba(79, 172, 254, 0.3);
            border-radius: 20px;
            padding: 4px 12px;
            font-size: 0.85rem;
            margin-right: 8px;
            margin-bottom: 8px;
        }
    </style>
    """, unsafe_allow_html=True)

# ----------------------------
# Speedometer / Gauge Chart
# ----------------------------
def create_gauge_chart(churn_prob_pct):
    """Generates an interactive Plotly gauge chart colored by risk zones."""
    # Determine color based on threshold
    if churn_prob_pct < 35:
        bar_color = "#10b981"  # Emerald Green
        status_text = "LOW RISK - SAFE"
    elif churn_prob_pct < 65:
        bar_color = "#f59e0b"  # Amber
        status_text = "MODERATE RISK"
    else:
        bar_color = "#ef4444"  # Coral Red
        status_text = "HIGH RISK - ATTRITION ALERT"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=churn_prob_pct,
        number={'suffix': "%", 'font': {'size': 42, 'color': '#ffffff', 'family': 'Inter'}},
        title={'text': f"<b>CHURN RISK METER</b><br><span style='color:{bar_color}; font-size:16px;'>{status_text}</span>", 'font': {'size': 18, 'color': '#94a3b8'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569", 'tickfont': {'color': '#94a3b8'}},
            'bar': {'color': bar_color, 'thickness': 0.3},
            'bgcolor': "rgba(255, 255, 255, 0.05)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.1)",
            'steps': [
                {'range': [0, 35], 'color': 'rgba(16, 185, 129, 0.15)'},
                {'range': [35, 65], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [65, 100], 'color': 'rgba(239, 68, 68, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "#ffffff", 'width': 3},
                'thickness': 0.8,
                'value': churn_prob_pct
            }
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#ffffff"},
        height=280,
        margin=dict(l=25, r=25, t=50, b=10)
    )
    return fig

# ----------------------------
# Feature Importance Chart
# ----------------------------
def create_feature_importance_chart(model, features):
    """Generates an interactive Plotly horizontal bar chart of Random Forest feature importances."""
    importances = model.feature_importances_
    clean_labels = {
        'days_since_last_login': 'Days Since Last Login',
        'subscription_duration_days': 'Subscription Tenure (Days)',
        'watch_hours_L30_days': 'Monthly Watch Hours',
        'age': 'Customer Age',
        'primary_device': 'Primary Device',
        'household_size': 'Household Size',
        'gender': 'Gender',
        'Monthly_Charge': 'Monthly Fee ($)',
        'subscription_plan': 'Subscription Tier',
        'payment_failures': 'Past Payment Failures',
        'auto_renew': 'Auto-Renew Status',
        'senior_user': 'Senior User (60+)'
    }
    
    df_imp = pd.DataFrame({
        'Feature': [clean_labels.get(f, f) for f in features],
        'Importance': importances
    }).sort_values('Importance', ascending=True)

    fig = px.bar(
        df_imp,
        x='Importance',
        y='Feature',
        orientation='h',
        color='Importance',
        color_continuous_scale=[[0, '#1c2541'], [0.5, '#4facfe'], [1.0, '#ff3366']],
        title="<b>Random Forest Feature Impact Breakdown</b>"
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#f8fafc'},
        coloraxis_showscale=False,
        height=400,
        margin=dict(l=10, r=20, t=40, b=20),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
        yaxis=dict(showgrid=False)
    )
    return fig

# ----------------------------
# Gemini AI Retention Copilot
# ----------------------------
def generate_retention_copilot(data_dict, churn_prob_pct, prediction):
    """
    Calls Google Gemini via official google.genai Client to generate:
    1. Root Cause Analysis
    2. Actionable Retention Strategy
    3. Personalized Re-engagement Email / Notification Copy
    Provides robust rule-based fallback if offline or API key is absent.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key and api_key != "your_gemini_api_key_here":
        try:
            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are a Principal Customer Retention Strategist for a premier streaming OTT service (like Netflix / Disney+).
            Analyze the following subscriber profile:

            - Predicted Churn Probability: {churn_prob_pct:.1f}%
            - Status: {'Likely to Churn' if prediction == 1 else 'Likely to Stay'}
            - Subscription Plan: {data_dict['subscription_plan']} (${data_dict['monthly_charge']}/mo)
            - Days Since Last Login: {data_dict['days_since_last_login']} days
            - Monthly Watch Hours: {data_dict['watch_hours']} hours
            - Payment Failures: {data_dict['payment_failures']}
            - Auto Renew: {data_dict['auto_renew']}
            - Subscription Tenure: {data_dict['subscription_duration_days']} days
            - Primary Device: {data_dict['primary_device']}
            - Household Size: {data_dict['household_size']}

            Provide a concise, high-value retention brief formatted in clean Markdown:
            ### 🔍 Executive Diagnosis
            Briefly identify the top 2 behavioral drivers behind this customer's score.

            ### 🎯 Tailored Retention Action Plan
            Provide 2-3 concrete business moves (e.g. specialized plan discount, content curation, payment grace period).

            ### ✉️ Ready-to-Send Outreach Copy
            Draft a warm, hyper-personalized re-engagement message (Email subject + short 3-line body or Push Notification) targeted directly to their device and plan.
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            # Fall back to intelligent rule-based synthesis if network/quota fails
            pass

    # Intelligent Rule-Based Fallback
    is_churn = (prediction == 1)
    login_days = data_dict['days_since_last_login']
    failures = data_dict['payment_failures']
    plan = data_dict['subscription_plan']
    device = data_dict['primary_device']

    diagnosis = []
    actions = []

    if login_days > 20:
        diagnosis.append(f"**Dormancy Warning:** Customer has been inactive for {login_days} days, the single highest churn indicator.")
        actions.append(f"Trigger an automated 'We miss you' watch-list re-engagement push notification optimized for {device}.")
    else:
        diagnosis.append(f"**Active Engagement:** Recent activity within {login_days} days indicates positive platform presence.")

    if failures > 0:
        diagnosis.append(f"**Friction Alert:** {failures} recent payment failure(s) create involuntary churn risk.")
        actions.append("Offer automated alternative payment method setup with a 7-day grace period.")

    if data_dict['auto_renew'] in ["No", 0]:
        actions.append(f"Incentivize auto-renewal renewal with a limited-time 15% discount on their {plan} plan.")

    if not actions:
        actions.append("Enroll customer in loyalty reward program and promote upcoming exclusive series premieres.")

    fallback_text = f"""
    ### 🔍 Executive Diagnosis
    * {" ".join(diagnosis)}
    * Current Churn Probability: **{churn_prob_pct:.1f}%** ({'High Risk' if is_churn else 'Low Risk'}).

    ### 🎯 Tailored Retention Action Plan
    """ + "\n".join([f"* {act}" for act in actions]) + f"""

    ### ✉️ Ready-to-Send Outreach Copy
    * **Subject:** We picked something special for your next watch on {device}!
    * **Body:** Hey there! It's been a little while since your last visit. We've just released trending shows in your favorite categories. Come back this week and enjoy 20% off your next {plan} billing cycle with promo code **RETENTION20**.
    """
    return fallback_text
