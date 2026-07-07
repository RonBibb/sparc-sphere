"""
BIC-threshold / model-selection sensitivity for the multi-domain fraction.

Re-scores the 1-vs-2 domain decision at a range of BIC thresholds and under AIC,
from the existing fits in data/two_vs_one_margins.csv (no re-fitting). Shows the
multi-domain population is not an artifact of the selection threshold.

Run from scripts/ :  <venv>/python3 bic_threshold_sensitivity.py
"""
import pandas as pd, numpy as np

m   = pd.read_csv("../data/two_vs_one_margins.csv")
cap = pd.read_csv("../data/tiered_spheres_capped.csv")
N   = len(m)

dBIC = m["bic_1"].values - m["bic_2"].values                  # >0 => 2 domains better (BIC)
dAIC = (m["chi2_1"].values + 2*2) - (m["chi2_2"].values + 2*4) # AIC: penalty 2k; k=2,4

rules = [
    ("BIC standard (dBIC>0)",        dBIC > 0),
    ("BIC 2-unit tie band (dBIC>2)", dBIC > 2),
    ("BIC stricter (dBIC>6)",        dBIC > 6),
    ("BIC very strong (dBIC>10)",    dBIC > 10),
    ("AIC (dAIC>0)",                 dAIC > 0),
]
print(f"N = {N} (one non-converged galaxy carries NaN and drops from all counts)")
print(f"{'rule':30}{'N>=2':>8}{'fraction':>10}")
for label, mask in rules:
    k = int(np.nansum(mask)); print(f"{label:30}{k:>8}{k/N:>9.1%}")

capm = int((cap["N_capped"] >= 2).sum())
print(f"\npipeline cross-check (N_capped>=2): {capm}/{N} = {capm/N:.1%}")

win2 = dBIC[dBIC > 0]; win1 = -dBIC[dBIC < 0]
print(f"\nmedian dBIC (2-domain preferred): {np.nanmedian(win2):+.1f}")
print(f"2-domain margins > 30 BIC: {int(np.nansum(dBIC > 30))}; max {np.nanmax(dBIC):+.0f}")
print(f"median 1-domain winning margin: {np.nanmedian(win1):+.1f}; max {np.nanmax(win1):+.1f}")
print(f"1-domain preferred by > 10 BIC: {int(np.nansum(-dBIC > 10))}")
