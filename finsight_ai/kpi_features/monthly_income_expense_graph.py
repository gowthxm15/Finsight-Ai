import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar

def prepare_monthly_data(df, selected_year):
    year_data = df[df['Date'].dt.year == selected_year].copy()
    monthly_summary = []

    for month in range(1, 13):
        month_data = year_data[year_data['Date'].dt.month == month]

        if 'Type' in df.columns:
            income = month_data[month_data['Type'].str.lower() == 'income']['Amount'].sum()
            expenses = abs(month_data[month_data['Type'].str.lower() == 'expense']['Amount'].sum())
        else:
            income = month_data[month_data['Amount'] > 0]['Amount'].sum()
            expenses = abs(month_data[month_data['Amount'] < 0]['Amount'].sum())

        monthly_summary.append({
            'Month': calendar.month_abbr[month],
            'Month_Name': calendar.month_name[month],
            'Month_Num': month,
            'Income': income,
            'Expenses': expenses,
            'Net_Cash_Flow': income - expenses,
            'Transaction_Count': len(month_data)
        })

    return pd.DataFrame(monthly_summary)

def create_monthly_chart(monthly_df, selected_year):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Income',
        x=monthly_df['Month'],
        y=monthly_df['Income'],
        marker_color='#10b981',
        text=[f'₹{val:,.0f}' if val > 0 else '' for val in monthly_df['Income']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Income: ₹%{y:,.2f}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        name='Expenses',
        x=monthly_df['Month'],
        y=monthly_df['Expenses'],
        marker_color='#ef4444',
        text=[f'₹{val:,.0f}' if val > 0 else '' for val in monthly_df['Expenses']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Expenses: ₹%{y:,.2f}<extra></extra>'
    ))

    fig.update_layout(
        title=f'Monthly Income vs Expenses - {selected_year}',
        xaxis_title='Month',
        yaxis_title='Amount (₹)',
        barmode='group',
        height=500,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')

    return fig

def display_yearly_summary(monthly_df, selected_year):
    year_income = monthly_df['Income'].sum()
    year_expenses = monthly_df['Expenses'].sum()
    year_net = year_income - year_expenses
    avg_monthly_income = year_income / 12
    avg_monthly_expense = year_expenses / 12

    # Metrics removed for cleaner UI
    return {
        'year_income': year_income,
        'year_expenses': year_expenses,
        'year_net': year_net,
        'avg_monthly_income': avg_monthly_income,
        'avg_monthly_expense': avg_monthly_expense
    }

def display_monthly_insights(monthly_df, yearly_stats):
    best_month_income = monthly_df.loc[monthly_df['Income'].idxmax()]
    worst_month_income = monthly_df.loc[monthly_df['Income'].idxmin()]
    best_month_cashflow = monthly_df.loc[monthly_df['Net_Cash_Flow'].idxmax()]
    worst_month_cashflow = monthly_df.loc[monthly_df['Net_Cash_Flow'].idxmin()]
    positive_months = len(monthly_df[monthly_df['Net_Cash_Flow'] > 0])
    total_months_with_data = len(monthly_df[monthly_df['Income'] > 0])

    with st.expander("📊 Monthly Performance Insights"):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**🏆 Best Performance:**")
            if best_month_income['Income'] > 0:
                st.write(f"• Highest Income: **{best_month_income['Month_Name']}** (₹{best_month_income['Income']:,.2f})")
            if best_month_cashflow['Net_Cash_Flow'] > 0:
                st.write(f"• Best Cash Flow: **{best_month_cashflow['Month_Name']}** (₹{best_month_cashflow['Net_Cash_Flow']:,.2f})")
            st.write(f"• **{positive_months}/{total_months_with_data}** months with positive cash flow")

        with col2:
            st.write("**⚠️ Areas for Improvement:**")
            if worst_month_income['Income'] > 0:
                st.write(f"• Lowest Income: **{worst_month_income['Month_Name']}** (₹{worst_month_income['Income']:,.2f})")
            if worst_month_cashflow['Net_Cash_Flow'] < 0:
                st.write(f"• Worst Cash Flow: **{worst_month_cashflow['Month_Name']}** (₹{worst_month_cashflow['Net_Cash_Flow']:,.2f})")
            if yearly_stats['year_income'] > 0:
                savings_rate = (yearly_stats['year_net'] / yearly_stats['year_income']) * 100
                st.write(f"• Savings Rate: **{savings_rate:.1f}%**")

def display_monthly_income_expense_graph(df):
    st.subheader("📊 Monthly Income vs Expenses")

    available_years = sorted(df['Date'].dt.year.unique(), reverse=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Analyze your monthly financial performance with detailed breakdowns.")
    with col2:
        selected_year = st.selectbox(
            "Select Year:",
            available_years,
            key="year_selector",
            help="Choose a year to view monthly breakdown"
        )

    monthly_df = prepare_monthly_data(df, selected_year)
    fig = create_monthly_chart(monthly_df, selected_year)
    st.plotly_chart(fig, use_container_width=True)

    yearly_stats = display_yearly_summary(monthly_df, selected_year)
    display_monthly_insights(monthly_df, yearly_stats)



    return monthly_df
