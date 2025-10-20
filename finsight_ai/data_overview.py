import streamlit as st
import pandas as pd
from dashboard import validate_data_structure 

def launch_data_overview():
    st.title("📋 Data Overview")
    st.markdown("---")

   
    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("⚠️ No financial data found. Please upload your data first.")
        st.info("👈 Go to the 'Upload Data' section to get started.")
        return

    df = st.session_state.df.copy()


    validated_df, error_message = validate_data_structure(df)

    if validated_df is None:
        st.error(f"❌ Data validation failed for overview: {error_message}")
        st.info("Please check your uploaded file's structure. It should contain 'Date' and 'Amount' columns.")
        return
    
    
    st.session_state.df = validated_df
    df = validated_df 

  
    if df.empty:
        st.error("❌ The uploaded and validated data appears to be empty.")
        return

    
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        try:
            df['Date'] = pd.to_datetime(df['Date'])
        except Exception as e:
            
            st.error(f"❌ Failed to convert 'Date' column after validation: {e}")
            return

    st.subheader("🔎 Dataset Summary")
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"• **Total Records:** {len(df):,}")
        st.write(f"• **Date Range:** {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
        st.write(f"• **Available Columns:** {len(df.columns)}")

    with col2:
        st.write("• **Column Names:**")
        for col in df.columns:
            st.write(f"   - {col}")

    st.subheader("📑 Data Types")
    dtypes = pd.DataFrame({
        "Column": df.columns,
        "Type": df.dtypes.astype(str).values
    })
    st.dataframe(dtypes, use_container_width=True, hide_index=True)

    st.subheader("📊 Data Preview")
    preview_rows = st.selectbox("Show rows:", [10, 25, 50, 100, 150], index=0)
    st.dataframe(df.head(preview_rows), use_container_width=True, hide_index=True)

    st.subheader("📈 Quick Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Date Range:**")
        st.write(f"• Earliest: {df['Date'].min().strftime('%B %d, %Y')}")
        st.write(f"• Latest: {df['Date'].max().strftime('%B %d, %Y')}")
        st.write(f"• Days Covered: {(df['Date'].max() - df['Date'].min()).days}")

    with col2:
        st.write("**Amount Analysis:**")
        st.write(f"• Maximum: ₹{df['Amount'].max():,.2f}")
        st.write(f"• Minimum: ₹{df['Amount'].min():,.2f}")
        st.write(f"• Average: ₹{df['Amount'].mean():,.2f}")

    with col3:
        st.write("**Data Quality:**")
        st.write(f"• Missing Values: {df.isnull().sum().sum()}")
        st.write(f"• Duplicate Rows: {df.duplicated().sum()}")
        st.write(f"• Unique Dates: {df['Date'].nunique()}")

