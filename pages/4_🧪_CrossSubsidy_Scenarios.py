
import streamlit as st, pandas as pd
from pathlib import Path
from src.calc import simulate_cross_subsidy

st.title("🧪 Cross-Subsidy & Tariff Scenarios")
WORKSPACE = st.secrets.get("workspace_key","default")
p = Path(f"tenants/{WORKSPACE}/data/wsa_input.csv")
if not p.exists(): st.warning("No WSA input found. Use Data Intake."); st.stop()
wsa = pd.read_csv(p)

xsub = st.slider("Apply cross-subsidy surcharge to non-indigent bills (%)", 0.0, 30.0, 5.0, 0.5)
st.caption("This simple model inflates non-indigent residential bills by the selected percentage.")

usage_profiles = {"lifeline": 6.0, "typical_low": 8.0, "typical": 12.0, "high": 20.0}
incomes = {"indigent_income": 1500.0, "low_income": 3000.0, "median_income": 8000.0}

rows = [simulate_cross_subsidy(r, usage_profiles, incomes, xsub) for _, r in wsa.iterrows()]
out = pd.DataFrame(rows)[["wsa_name","bill_typical_non_indigent","bill_typical_non_indigent_xsub","aff_typical_median"]]
out["delta_bill_non_indigent"] = out["bill_typical_non_indigent_xsub"] - out["bill_typical_non_indigent"]
st.dataframe(out.head())

csv = out.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download scenario CSV", data=csv, file_name="wsa_xsub_scenario.csv", mime="text/csv")
