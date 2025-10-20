import streamlit as st
import pandas as pd
import plotly.express as px

def display_top_expense_categories(df):
    """Display pie chart of top 5 expense categories"""
    
    st.subheader("🏷️ Top 5 Expense Categories")
    # Check if Category column exists
    if 'Category' not in df.columns:
        st.warning("⚠️ 'Category' column not found in the dataset.")
        return
    
    # Filter only expenses (negative Amount or labeled 'expense')
    if 'Type' in df.columns:
        expense_df = df[df['Type'].str.lower() == 'expense'].copy()
    else:
        expense_df = df[df['Amount'] < 0].copy()
    
    # Convert amounts to positive for charting
    expense_df['Amount'] = expense_df['Amount'].abs()
    
    # Group by category and sum expenses
    category_summary = expense_df.groupby('Category')['Amount'].sum().sort_values(ascending=False).head(5).reset_index()
    
    # If no data available
    if category_summary.empty:
        st.info("No expense data available to display top categories.")
        return

    # Plot pie chart
    fig = px.pie(
        category_summary,
        names='Category',
        values='Amount',
        title='Top 5 Expense Categories',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig, use_container_width=True)
