import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.model_loader import load_dataset
from utils.ui_components import inject_custom_css

st.set_page_config(
    page_title="Executive Dashboard | OTT Platform",
    page_icon="📊",
    layout="wide"
)

inject_custom_css()

st.markdown("<h1 class='hero-title'>📊 Executive Streaming Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Holistic business metrics, subscriber retention trends, and behavioral analytics</p>", unsafe_allow_html=True)

df = load_dataset()

if df is None:
    st.error("Platform dataset not found. Please verify `Data/Cleaned Data/users_cleaned_final.csv`.")
    st.stop()

# ----------------------------
# Sidebar / Top Filters
# ----------------------------
st.markdown("<div class='section-header'>🔍 Interactive Segment Filters</div>", unsafe_allow_html=True)

f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    plans = ["All Plans"] + sorted(list(df["subscription_plan"].dropna().unique()))
    selected_plan = st.selectbox("Subscription Tier", plans)

with f_col2:
    devices = ["All Devices"] + sorted(list(df["primary_device"].dropna().unique()))
    selected_device = st.selectbox("Primary Device", devices)

with f_col3:
    senior_opts = ["All Users", "Senior Users (60+)", "Standard Age (<60)"]
    selected_senior = st.selectbox("Demographic Segment", senior_opts)

# Apply filters
filtered_df = df.copy()
if selected_plan != "All Plans":
    filtered_df = filtered_df[filtered_df["subscription_plan"] == selected_plan]
if selected_device != "All Devices":
    filtered_df = filtered_df[filtered_df["primary_device"] == selected_device]
if selected_senior == "Senior Users (60+)":
    filtered_df = filtered_df[filtered_df["senior_user"] == 1]
elif selected_senior == "Standard Age (<60)":
    filtered_df = filtered_df[filtered_df["senior_user"] == 0]

# ----------------------------
# Top-Line Executive KPIs
# ----------------------------
total_subscribers = len(filtered_df)
churn_total = int(filtered_df["churn"].sum())
churn_rate = (churn_total / total_subscribers * 100) if total_subscribers > 0 else 0
total_mrr = filtered_df["Monthly_Charge"].sum() if "Monthly_Charge" in filtered_df.columns else 0
avg_watch = filtered_df["watch_hours_L30_days"].mean() if "watch_hours_L30_days" in filtered_df.columns else 0
avg_login_gap = filtered_df["days_since_last_login"].mean() if "days_since_last_login" in filtered_df.columns else 0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.metric("Total Subscribers", f"{total_subscribers:,}")
with kpi2:
    st.metric("Segment Churn Rate", f"{churn_rate:.1f}%")
with kpi3:
    st.metric("Total Monthly Revenue (MRR)", f"${total_mrr:,.0f}")
with kpi4:
    st.metric("Avg Watch Hours (30d)", f"{avg_watch:.1f} hrs")
with kpi5:
    st.metric("Avg Inactivity Gap", f"{avg_login_gap:.1f} days")

# ----------------------------
# Visual Analytics Grid
# ----------------------------
st.markdown("<div class='section-header'>📈 Behavioral & Attrition Drivers</div>", unsafe_allow_html=True)

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    # 1. Churn Rate by Subscription Tier
    tier_summary = df.groupby("subscription_plan").agg(
        Total=('churn', 'count'),
        Churned=('churn', 'sum'),
        Avg_Charge=('Monthly_Charge', 'mean')
    ).reset_index()
    tier_summary["Churn_Rate"] = (tier_summary["Churned"] / tier_summary["Total"]) * 100

    fig_tier = px.bar(
        tier_summary,
        x="subscription_plan",
        y="Churn_Rate",
        color="Churn_Rate",
        color_continuous_scale=[[0, '#4facfe'], [1.0, '#ff3366']],
        title="<b>Churn Rate by Subscription Plan (%)</b>",
        labels={"subscription_plan": "Subscription Plan", "Churn_Rate": "Churn Rate (%)"}
    )
    fig_tier.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#f8fafc'},
        coloraxis_showscale=False,
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_tier, use_container_width=True)

with row1_col2:
    # 2. Days Since Last Login vs Churn (The #1 Driver)
    fig_login = px.histogram(
        filtered_df,
        x="days_since_last_login",
        color=filtered_df["churn"].map({0: "Retained (Safe)", 1: "Churned"}),
        barmode="overlay",
        nbins=35,
        color_discrete_map={"Retained (Safe)": "#10b981", "Churned": "#ff3366"},
        title="<b>Login Inactivity vs Churn Distribution</b>",
        labels={"days_since_last_login": "Days Since Last Login"}
    )
    fig_login.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#f8fafc'},
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", y=-0.2)
    )
    st.plotly_chart(fig_login, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    # 3. Monthly Watch Hours vs Churn
    fig_watch = px.box(
        filtered_df,
        x=filtered_df["churn"].map({0: "Retained", 1: "Churned"}),
        y="watch_hours_L30_days",
        color=filtered_df["churn"].map({0: "Retained", 1: "Churned"}),
        color_discrete_map={"Retained": "#4facfe", "Churned": "#ff3366"},
        title="<b>Monthly Watch Hours by Retention Status</b>",
        labels={"x": "Status", "watch_hours_L30_days": "Watch Hours (Last 30 Days)"}
    )
    fig_watch.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#f8fafc'},
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
        showlegend=False
    )
    st.plotly_chart(fig_watch, use_container_width=True)

with row2_col2:
    # 4. Device Usage Breakdown
    device_summary = filtered_df.groupby("primary_device")["churn"].agg(["count", "mean"]).reset_index()
    device_summary["Churn_Pct"] = device_summary["mean"] * 100
    
    fig_dev = px.bar(
        device_summary,
        x="primary_device",
        y="count",
        color="Churn_Pct",
        color_continuous_scale="Viridis",
        title="<b>Subscribers by Device & Churn Rate</b>",
        labels={"count": "Total Subscribers", "primary_device": "Device", "Churn_Pct": "Churn %"}
    )
    fig_dev.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#f8fafc'},
        coloraxis_colorbar=dict(title="Churn %"),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_dev, use_container_width=True)

# ----------------------------
# SQL Business Query Showcase
# ----------------------------
st.markdown("<div class='section-header'>💾 SQL Data Engineering & Query Insights</div>", unsafe_allow_html=True)

with st.expander("🔍 View Production SQL Queries executed on MySQL Database", expanded=False):
    sql_tab1, sql_tab2, sql_tab3 = st.tabs(["Churn by Plan", "Auto-Renew Impact", "High-Value Inactive Users"])

    with sql_tab1:
        st.code("""
-- Query: Churn Rate by Subscription Plan
SELECT 
    subscription_plan,
    COUNT(*) AS total_subscribers,
    SUM(churn) AS churned_subscribers,
    ROUND((SUM(churn) / COUNT(*)) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(Monthly_Charge), 2) AS avg_monthly_revenue
FROM users
GROUP BY subscription_plan
ORDER BY churn_rate_pct DESC;
        """, language="sql")
        st.dataframe(tier_summary[["subscription_plan", "Total", "Churned", "Churn_Rate", "Avg_Charge"]], use_container_width=True)

    with sql_tab2:
        st.code("""
-- Query: Auto-Renew Status vs Customer Churn
SELECT 
    auto_renew,
    COUNT(*) AS total_users,
    SUM(churn) AS churned_users,
    ROUND((SUM(churn) / COUNT(*)) * 100, 2) AS churn_pct
FROM users
GROUP BY auto_renew;
        """, language="sql")
        ar_summary = df.groupby("auto_renew")["churn"].agg(["count", "sum"]).reset_index()
        ar_summary["Churn_Rate_%"] = (ar_summary["sum"] / ar_summary["count"]) * 100
        ar_summary.columns = ["Auto Renew", "Total Users", "Churned Users", "Churn Rate (%)"]
        st.dataframe(ar_summary, use_container_width=True)

    with sql_tab3:
        st.code("""
-- Query: At-Risk High Value Customers (Premium plan + >20 days inactivity)
SELECT 
    user_id, email, subscription_plan, Monthly_Charge,
    days_since_last_login, watch_hours_L30_days
FROM users
WHERE is_active = 'True' 
  AND subscription_plan IN ('Premium', 'Premium+') 
  AND days_since_last_login > 20
ORDER BY Monthly_Charge DESC, days_since_last_login DESC
LIMIT 10;
        """, language="sql")
