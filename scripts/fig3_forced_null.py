# fig3_forced_null.py  --  Figure 3 for the halo-spheres letter.
#
# Visualizes the FORCED-FIT ASYMMETRY (the reviewer's "most important new result"):
#   - INNER component: forced fits reproduce the winners' below-relation offset
#     -> NOT diagnostic (the null fires; Mann-Whitney p ~ 0.10).
#   - OUTER component: forced fits are driven FAR below the relation while winners
#     stay near it -> the discriminator (Mann-Whitney p ~ 2e-4).
# One tier survives forcing, the other does not. That asymmetry is the evidence
# that the OUTER domain tracks a genuine halo component.
#
# INPUT: data/forced_component_null.csv  (produced by forced_component_null.py;
#        columns: galaxy, group in {winner,forced}, vflat, in_off, out_off)
# OUTPUT: figures/fig3_forced_null.png   (dpi 240, publication)
#
# Path-independent: resolves data/ and figures/ relative to THIS script's location,
# so it runs correctly from any working directory.
#
# Numbers the figure should reproduce (from the v0.7 text / forced_component_null.py):
#   inner: winner vs forced indistinguishable, MW p ~ 0.10  (NOT diagnostic)
#   outer: winner median ~ -0.95 sigma, forced median ~ -3.44 sigma, MW p ~ 2e-4
# If the recomputed numbers differ materially, STOP and reconcile (text is frozen).

import os
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- resolve paths relative to this script, not the CWD ---
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "forced_component_null.csv")
OUT  = os.path.join(ROOT, "figures", "fig3_forced_null.png")

if not os.path.exists(DATA):
    raise SystemExit(f"Missing {DATA}\n  -> run forced_component_null.py first (from scripts/).")

D = pd.read_csv(DATA)
win = D[D.group == "winner"]
forc = D[D.group == "forced"]

# --- recompute the headline stats so the figure is self-consistent with the text ---
def med(x): return np.nanmedian(x.values)
inner_win, inner_forc = win.in_off.dropna(), forc.in_off.dropna()
outer_win, outer_forc = win.out_off.dropna(), forc.out_off.dropna()
p_inner = stats.mannwhitneyu(inner_forc, inner_win).pvalue
p_outer = stats.mannwhitneyu(outer_forc, outer_win).pvalue
print(f"INNER: winner median {med(win.in_off):+.2f}s, forced {med(forc.in_off):+.2f}s, MW p={p_inner:.2e}")
print(f"OUTER: winner median {med(win.out_off):+.2f}s, forced {med(forc.out_off):+.2f}s, MW p={p_outer:.2e}")

# --- plot: two panels (INNER = the null, OUTER = the discriminator) ---
fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.4), sharey=True)
groups = [("Selected", "winner"), ("Forced", "forced")]
colors = {"winner": "#2c7fb8", "forced": "#d95f0e"}

def panel(ax, col, title, pval, note):
    data = [D[D.group == g][col].dropna().values for lbl, g in groups]
    bp = ax.boxplot(data, positions=[1, 2], widths=0.5, patch_artist=True,
                    showfliers=False, medianprops=dict(color="black", lw=1.6), zorder=2)
    for patch, (lbl, g) in zip(bp["boxes"], groups):
        patch.set_facecolor(colors[g]); patch.set_alpha(0.35)
    rng = np.random.default_rng(0)
    for i, (lbl, g) in enumerate(groups, start=1):
        v = D[D.group == g][col].dropna().values
        x = i + rng.uniform(-0.13, 0.13, size=len(v))
        ax.scatter(x, v, s=18, color=colors[g], alpha=0.75, edgecolor="none", zorder=3)
    ax.axhline(0.0, color="0.5", lw=1.0, ls="--", zorder=1)   # the single-domain relation
    ax.set_xticks([1, 2]); ax.set_xticklabels(["Selected", "Forced"])
    ax.set_title(title, fontsize=11)
    ax.text(0.5, 0.03, f"MW $p={pval:.1g}$\n{note}", transform=ax.transAxes,
            ha="center", va="bottom", fontsize=9,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="0.7", alpha=0.9))

panel(axes[0], "in_off", "Inner component", p_inner, "reproduced under forcing\n(not diagnostic)")
panel(axes[1], "out_off", "Outer component", p_outer, "not reproduced\n(diagnostic)")
axes[0].set_ylabel(r"offset from single-domain $\rho_0$--$a$ relation [$\sigma$]")
fig.suptitle("Forced-fit null: the inner offset is reproducible, the outer is not",
             fontsize=11.5, y=0.98)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(OUT, dpi=240, bbox_inches="tight")
print(f"wrote {OUT}")
