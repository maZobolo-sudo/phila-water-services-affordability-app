
import streamlit as st, pandas as pd, numpy as np
from pathlib import Path
from src.calc import wsa_metrics_row, AFFORDABILITY_THRESHOLD

st.title("📐 Affordability Metrics")
WORKSPACE = st.secrets.get("workspace_key","default")
p = Path(f"tenants/{WORKSPACE}/data/wsa_input.csv")
if not p.exists():
    st.warning("No WSA input found. Use Data Intake or rely on the demo sample on Overview."); st.stop()
wsa = pd.read_csv(p)

st.subheader("Profiles")
col1, col2 = st.columns(2)
with col1:
    lifeline = st.number_input("Lifeline usage (kL/month)", value=6.0, step=0.5)
    typical_low = st.number_input("Typical low-income usage (kL)", value=8.0, step=0.5)
    typical = st.number_input("Typical usage (kL)", value=12.0, step=0.5)
    high = st.number_input("High usage (kL)", value=20.0, step=0.5)
usage_profiles = {"lifeline": lifeline, "typical_low": typical_low, "typical": typical, "high": high}

with col2:
    indigent_income = st.number_input("Indigent monthly income (ZAR)", value=1500.0, step=50.0)
    low_income = st.number_input("Low-income monthly income (ZAR)", value=3000.0, step=50.0)
    median_income = st.number_input("Median monthly income (ZAR)", value=8000.0, step=100.0)
incomes = {"indigent_income": indigent_income, "low_income": low_income, "median_income": median_income}

rows = []
for _, r in wsa.iterrows():
    rows.append(wsa_metrics_row(r, usage_profiles, incomes))

out = pd.DataFrame(rows)
st.write(f"Affordability threshold = {AFFORDABILITY_THRESHOLD:.0%}")
st.dataframe(out.head())

st.subheader("Key flags (above threshold at typical usage, median income)")
viol = out[ out["aff_typical_median"] > AFFORDABILITY_THRESHOLD ][["wsa_name","aff_typical_median","indigent_share","fbw_kl","annual_revenue","unemployment_rate"]].sort_values("aff_typical_median", ascending=False)
st.dataframe(viol)

csv = out.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download metrics CSV", data=csv, file_name="wsa_affordability_metrics.csv", mime="text/csv")
