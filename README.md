# phila-water-services-affordability-app
This Streamlit app evaluates "potable" water service affordability across Water Service Authorities (WSAs) in South Africa.
**Model used:** Rule-based affordability model (block tariffs + FBW + income anchors), with scenario simulation.  
```markdown
# ⚖️ WSA Affordability Tracker (South Africa)

This Streamlit app evaluates **water service affordability** across Water Service Authorities (WSAs) in South Africa.

## Methodology
- **Inputs per WSA:** FBW (Free Basic Water) allocation, indigent share, tariff block structure, cross-subsidy %, annual revenue, unemployment rate
- **Affordability model:** Household water bills computed via block tariff rules
- **Benchmarks:** Bills vs. income anchors (indigent, low, median income)
- **Threshold:** 3% of income as affordability limit (editable)
- **Scenarios:** Apply cross-subsidy surcharges and simulate impact

## Outputs
- Affordability metrics by WSA
- Flags for WSAs above threshold
- Revenue and unemployment context
- Exportable PDF and PPTX reports

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
