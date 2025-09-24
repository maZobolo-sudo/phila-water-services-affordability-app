
import streamlit as st, pandas as pd
st.title("🏁 Overview")
st.write("This app evaluates **water service affordability** at WSA level in South Africa.")
st.markdown("""
**Inputs expected per WSA:**
- `wsa_id`, `wsa_name`
- `households` (monthly-billed households)
- `indigent_share` (0–1)
- `fbw_kl` (kL/month HH) – Free Basic Water offered to indigent HHs
- Tariff blocks & prices: `b1_kl`, `b1_price`, `b2_kl`, `b2_price`, `b3_price`
- `cross_subsidy_pct` (optional surcharge on non-indigent residential)
- `annual_revenue` (ZAR)
- `unemployment_rate` (0–1)
""")
st.caption("You can also override income & usage profiles on the Metrics page.")
