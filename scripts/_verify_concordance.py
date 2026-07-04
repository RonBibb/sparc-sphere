import numpy as np, pandas as pd
from scipy import stats
m=pd.read_csv("../data/spatial_coincidence_capped.csv")
print("n =",len(m))
rho,p=stats.spearmanr(m.r_cross,m.r_shell)
print(f"Spearman(r_cross,r_shell) = {rho:.3f}  p={p:.2e}")
# permutation on fractional offset
obs=np.median(np.abs(m.r_cross-m.r_shell)/m.rmax)
rng=np.random.default_rng(0)
perm=np.array([np.median(np.abs(m.r_cross.values-m.r_shell.sample(frac=1,random_state=rng.integers(1_000_000_000)).values)/m.rmax.values) for _ in range(5000)])
print(f"median frac offset = {obs:.3f}  perm-null median = {np.median(perm):.3f}  p(obs<=null) = {(perm<=obs).mean():.4f}")
# partial spearman controlling reff: residualize ranks
def resid_on(y,x):
    ry=stats.rankdata(y); rx=stats.rankdata(x)
    b=np.polyfit(rx,ry,1); return ry-np.polyval(b,rx)
pr,pp=stats.spearmanr(resid_on(m.r_cross,m.reff),resid_on(m.r_shell,m.reff))
print(f"partial Spearman (control reff) = {pr:.3f}  p={pp:.2e}")
print(f"Spearman(r_cross,reff) = {stats.spearmanr(m.r_cross,m.reff)[0]:.3f}")
