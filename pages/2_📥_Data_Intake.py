
import streamlit as st, pandas as pd
from pathlib import Path

st.title("📥 Data Intake – WSA Table")
up = st.file_uploader("Upload CSV with the columns listed on Overview", type=["csv"])
if not up:
    st.info("Upload your WSA CSV. A tiny demo sample is present by default.")
else:
    df = pd.read_csv(up)
    WORKSPACE = st.secrets.get("workspace_key","default")
    p = Path(f"tenants/{WORKSPACE}/data/wsa_input.csv"); p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False); st.success(f"Saved to {p}")
    st.dataframe(df.head())
