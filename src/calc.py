
import numpy as np
import pandas as pd

AFFORDABILITY_THRESHOLD = 0.03  # 3% of income as default

def bill_for_usage(usage_kl, blocks, prices, fbw_kl=0.0):
    use = max(0.0, usage_kl - fbw_kl)
    cost = 0.0
    prev = 0.0
    for b, p in zip(blocks, prices):
        slab = min(use, b - prev)
        if slab > 0:
            cost += slab * p
            use -= slab
            prev = b
        if use <= 0:
            break
    return cost

def affordability_pct(income, bill):
    if income <= 0:
        return np.nan
    return bill / income

def wsa_metrics_row(row, usage_profiles, incomes, apply_fbw_for_indigent=True):
    blocks = [row.get("b1_kl", 6), row.get("b2_kl", 15), np.inf]
    prices = [row.get("b1_price", 0.0), row.get("b2_price", 0.0), row.get("b3_price", 0.0)]
    indigent_share = min(max(row.get("indigent_share", 0.0), 0.0), 1.0)
    fbw = row.get("fbw_kl", 0.0) if apply_fbw_for_indigent else 0.0

    bills = {}
    for k, use in usage_profiles.items():
        bills[f"bill_{k}_indigent"] = bill_for_usage(use, blocks, prices, fbw_kl=fbw)
        bills[f"bill_{k}_non_indigent"] = bill_for_usage(use, blocks, prices, fbw_kl=0.0)

    aff = {
        "aff_lifeline_indigent": affordability_pct(incomes["indigent_income"], bills["bill_lifeline_indigent"]),
        "aff_typical_low_indigent": affordability_pct(incomes["indigent_income"], bills["bill_typical_low_indigent"]),
        "aff_typical_nonindigent_low": affordability_pct(incomes["low_income"], bills["bill_typical_non_indigent"]),
        "aff_typical_median": affordability_pct(incomes["median_income"], bills["bill_typical_non_indigent"]),
    }

    flags = {f"{k}_above_thresh": (v is not None and v > AFFORDABILITY_THRESHOLD) for k, v in aff.items()}

    households = max(1, int(row.get("households", 0) or 0))
    indigent_hh = int(round(indigent_share * households))
    fbw_coverage_pct = indigent_share

    xsub_pct = row.get("cross_subsidy_pct", 0.0) or 0.0
    if xsub_pct:
        for k in list(bills.keys()):
            if "non_indigent" in k:
                bills[k + "_xsub"] = bills[k] * (1 + xsub_pct/100.0)

    out = {
        "wsa_id": row.get("wsa_id", ""),
        "wsa_name": row.get("wsa_name", ""),
        "households": households,
        "indigent_share": indigent_share,
        "fbw_kl": row.get("fbw_kl", 0.0),
        "fbw_coverage_pct": fbw_coverage_pct,
        "annual_revenue": row.get("annual_revenue", np.nan),
        "unemployment_rate": row.get("unemployment_rate", np.nan),
    }
    out.update(bills); out.update(aff); out.update(flags)
    return out

def simulate_cross_subsidy(row, usage_profiles, incomes, xsub_pct):
    row2 = row.copy()
    row2["cross_subsidy_pct"] = xsub_pct
    return wsa_metrics_row(row2, usage_profiles, incomes)
