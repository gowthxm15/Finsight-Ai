# kpi_features/monthly_cashflow_trend.py

import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

def prepare_cashflow_data(df, selected_year):
    """Prepare monthly net cash flow data for the selected year."""
    
    df_year = df[df['Date'].dt.year == selected_year].copy()
    

    monthly_data = []

    for month in range(1, 13):
        month_df = df_year[df_year['Date'].dt.month == month]
        

        if 'Type' in month_df.columns:
            income = month_df[month_df['Type'].str.lower() == 'income']['Amount'].sum()
            expenses = month_df[month_df['Type'].str.lower() == 'expense']['Amount'].sum()
        else:
            income = month_df[month_df['Amount'] > 0]['Amount'].sum()
            expenses = month_df[month_df['Amount'] < 0]['Amount'].sum()
        
        net_cashflow = income + expenses  
        
        monthly_data.append({
            'Month': calendar.month_abbr[month],
            'Net_Cash_Flow': net_cashflow
        })

    return pd.DataFrame(monthly_data)

def display_cashflow_trend(df):
    """Display the line chart of monthly net cash flow."""
    st.subheader("📈 Monthly Net Cash Flow Trend")

    available_years = sorted(df['Date'].dt.year.unique(), reverse=True)
    selected_year = st.selectbox("Select Year", available_years, key="cashflow_year")

    monthly_cashflow_df = prepare_cashflow_data(df, selected_year)

    fig = px.line(
        monthly_cashflow_df,
        x="Month",
        y="Net_Cash_Flow",
        title=f"Net Cash Flow Trend - {selected_year}",
        markers=True,
        labels={"Net_Cash_Flow": "Net Cash Flow (₹)"},
        template="plotly_white"
    )

    fig.update_traces(line_color="#0f3c61", marker_color="#10b981")
    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)
