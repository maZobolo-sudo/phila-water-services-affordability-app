
import streamlit as st, pandas as pd
from pathlib import Path
from src.calc import wsa_metrics_row
from src.reporting import make_pdf_report, make_pptx

st.title("📝 Reports & Exports")
WORKSPACE = st.secrets.get("workspace_key","default")
p = Path(f"tenants/{WORKSPACE}/data/wsa_input.csv")
if not p.exists(): st.warning("No WSA input found. Use Data Intake."); st.stop()
wsa = pd.read_csv(p)

usage_profiles = {"lifeline": 6.0, "typical_low": 8.0, "typical": 12.0, "high": 20.0}
incomes = {"indigent_income": 1500.0, "low_income": 3000.0, "median_income": 8000.0}

rows = [wsa_metrics_row(r, usage_profiles, incomes) for _, r in wsa.iterrows()]
pdf = make_pdf_report(rows, f"tenants/{WORKSPACE}/reports/wsa_affordability_report.pdf")
with open(pdf,"rb") as f:
    st.download_button("⬇️ Download PDF Report", f, file_name="wsa_affordability_report.pdf")

ppt = make_pptx(rows, f"tenants/{WORKSPACE}/reports/wsa_affordability_slides.pptx")
with open(ppt,"rb") as f:
    st.download_button("⬇️ Download Slides (PPTX)", f, file_name="wsa_affordability_slides.pptx")
