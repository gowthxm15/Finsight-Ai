import streamlit as st
from utils.file_handler import load_excel_file

def upload_data():
    st.title("📤 Upload Excel File")
    uploaded_file = st.file_uploader("Upload your corporate financial Excel file", type=["xlsx", "xls"])
    
    if uploaded_file:
        try:
            df = load_excel_file(uploaded_file)
            st.session_state.df = df
            st.success("✅ File uploaded and loaded successfully!")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")
