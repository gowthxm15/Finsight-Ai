# kpi_features/financial_summary_cards.py
import streamlit as st
import pandas as pd
from datetime import datetime

def calculate_financial_metrics(df):
    """Calculate financial metrics from the dataframe"""
    
    total_income = 0
    total_expense = 0

    if 'Type' in df.columns and 'Amount' in df.columns:
        income_mask = (df['Type'].str.lower() == 'income') | (df['Amount'] > 0)
        total_income = df[income_mask]['Amount'].sum()

        expense_mask = (df['Type'].str.lower() == 'expense') | (df['Amount'] < 0)
        total_expense = abs(df[expense_mask]['Amount'].sum())

    elif 'Amount' in df.columns:
        total_income = df[df['Amount'] > 0]['Amount'].sum()
        total_expense = abs(df[df['Amount'] < 0]['Amount'].sum())

    net_cash_flow = total_income - total_expense
    total_transactions = len(df)

    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'net_cash_flow': net_cash_flow,
        'total_transactions': total_transactions
    }

def display_financial_summary_cards(df):
    """Display financial summary cards without deltas"""

    st.subheader("📈 Financial Overview")

    metrics = calculate_financial_metrics(df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Total Income", f"₹{metrics['total_income']:,.2f}")

    with col2:
        st.metric("💸 Total Expenses", f"₹{metrics['total_expense']:,.2f}")

    with col3:
        st.metric("💡 Net Cash Flow", f"₹{metrics['net_cash_flow']:,.2f}")

    with col4:
        st.metric("📊 Total Transactions", metrics['total_transactions'])
