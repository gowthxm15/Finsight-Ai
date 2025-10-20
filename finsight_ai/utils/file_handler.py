import pandas as pd
import io

def load_excel_file(uploaded_file):
    try:
        return pd.read_excel(uploaded_file)
    except Exception as e:
        raise ValueError(f"❌ Failed to load Excel file: {e}")
