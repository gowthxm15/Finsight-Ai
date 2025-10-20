# dashboard.py
import streamlit as st
import pandas as pd
from datetime import datetime


from kpi_features.financial_summary_cards import display_financial_summary_cards
from kpi_features.monthly_income_expense_graph import display_monthly_income_expense_graph
from kpi_features.top_expense_categories import display_top_expense_categories
from kpi_features.monthly_cashflow_trend import display_cashflow_trend

def validate_data_structure(df):
    """Validate and standardize the data structure"""
    if 'Date' in df.columns:
        pass
    elif 'date' in df.columns:
        df = df.rename(columns={'date': 'Date'})
    else:
        return None, "❌ Date column not found."

    if 'Amount' not in df.columns and 'amount' not in df.columns:
        return None, "❌ Amount column not found."

    column_mapping = {
        'date': 'Date',
        'amount': 'Amount',
        'type': 'Type',
        'category': 'Category',
        'description': 'Description'
    }

    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})

    try:
        df['Date'] = pd.to_datetime(df['Date'])
    except Exception as e:
        return None, f"❌ Unable to parse Date column: {str(e)}"

    try:
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df = df.dropna(subset=['Amount'])
    except Exception as e:
        return None, f"❌ Unable to parse Amount column: {str(e)}"

    return df, None

def launch_dashboard():
    """Main dashboard function with modular KPI features"""
    st.title("📊 Financial KPI Dashboard")
    st.markdown("---")

    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("⚠️ No financial data found. Please upload your data first.")
        st.info("👈 Go to the 'Upload Data' section to get started.")
        return

    df = st.session_state.df
    validated_df, error_message = validate_data_structure(df.copy())

    if validated_df is None:
        st.error(error_message)
        return

    st.session_state.df = validated_df
    df = validated_df

    if df.empty:
        st.error("❌ The uploaded data appears to be empty.")
        return

    #1
    try:
        display_financial_summary_cards(df)
        st.markdown("---")
    except Exception as e:
        st.error(f"❌ Error displaying financial summary: {str(e)}")

    #2
    try:
        display_monthly_income_expense_graph(df)
        st.markdown("---")
    except Exception as e:
        st.error(f"❌ Error displaying monthly graph: {str(e)}")

    #3
    try:
        display_top_expense_categories(df)
        st.markdown("---")
    except Exception as e:
        st.error(f"❌ Error displaying top expenses: {str(e)}")

    # 4
    try:
        display_cashflow_trend(df)
        st.markdown("---")
    except Exception as e:
        st.error(f"❌ Error displaying cash flow trend: {str(e)}")

    
