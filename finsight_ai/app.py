import streamlit as st
from chat import launch_chat
from upload import upload_data
from dashboard import launch_dashboard
from data_overview import launch_data_overview



st.set_page_config(page_title="FinSight AI", page_icon="📊", layout="wide")


st.sidebar.title("📊 FinSight AI")


section = st.sidebar.selectbox(
    "Choose Section",
    ["📁 Data", "📈 Analysis", "📥 Report"]
)


if section == "📁 Data":
    page = st.sidebar.radio("Data Tools", ["📤 Upload Data", "🔍 Data Overview"], label_visibility="collapsed")

elif section == "📈 Analysis":
    page = st.sidebar.radio("Analysis Tools", ["🧠 Finbot", "📊 KPI Dashboard"], label_visibility="collapsed")

elif section == "📥 Report":
    page = st.sidebar.radio("Download", ["📥 Download Report"], label_visibility="collapsed")

#routing
if page == "📤 Upload Data":
    upload_data()

elif page == "🔍 Data Overview":
    launch_data_overview()

elif page == "🧠 Finbot":
    launch_chat()

elif page == "📊 KPI Dashboard":
    launch_dashboard()

elif page == "📥 Download Report":
    st.subheader("📥 Download Report (Coming Soon...)")
    st.info("This feature will allow you to generate Excel and PDF financial reports.")
