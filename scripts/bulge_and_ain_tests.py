# Test 1: does BULGE presence predict multi-sphere selection beyond mass?
# Test 2: for capped 2-sphere galaxies, is a_in ~ the same galaxy's single-Burkert a
#         (additive) or a_in << a_single (reorganized)?
import os, numpy as np, pandas as pd, warnings
from scipy import stats
from scipy.optimize import minimize
warnings.filterwarnings("ignore")
import tiered_spheres as ts, tiered_spheres_capped as tc

cap=pd.read_csv("../data/processed/tiered_spheres_capped.csv")
cat=pd.read_csv("../data/raw/sparc_sample123.csv")

# ---------- bulge flag from rotmod files (Vbul column) ----------
def has_bulge(g):
    p=f"{ts.DATA}/{g}_rotmod.dat"
    if not os.path.exists(p): return np.nan
    try:
        arr=np.loadtxt(p)
        if arr.ndim==1: arr=arr[None,:]
        return float((np.abs(arr[:,5])>0).any())
    except Exception: return np.nan

m=cap.merge(cat,left_on='galaxy',right_on='Galaxy',how='left')
m['bulge']=[has_bulge(g) for g in m.galaxy]
m['multi']=(m.N_capped>=2).astype(int)
m=m.dropna(subset=['bulge','logM_star'])
print(f"galaxies with bulge flag: {len(m)};  bulge-bearing: {int(m.bulge.sum())} ({100*m.bulge.mean():.0f}%)")
print(f"  bulge fraction | multi-sphere: {100*m.loc[m.multi==1,'bulge'].mean():.0f}%   single: {100*m.loc[m.multi==0,'bulge'].mean():.0f}%")

# logistic regression: multi ~ logM* (+ bulge), LR test
def logreg(Xc,d):
    X=np.column_stack([np.ones(len(d))]+[(d[c]-d[c].mean())/(d[c].std() if d[c].std()>0 else 1) for c in Xc])
    y=d['multi'].values.astype(float)
    nll=lambda b: -np.sum(y*(X@b)-np.logaddexp(0,X@b))
    r=minimize(nll,np.zeros(X.shape[1]),method='BFGS')
    return r.x,-r.fun
_,ll0=logreg(['logM_star'],m)
bf,ll1=logreg(['logM_star','bulge'],m)
chi2=2*(ll1-ll0); p=stats.chi2.sf(chi2,1)
print(f"\nTEST 1 — bulge beyond mass: LR chi2={chi2:.2f}  p={p:.4f}  coef(bulge|mass)={bf[-1]:+.2f}")
print("  -> "+("SURVIVES mass control" if p<0.05 else "absorbed by mass"))
# also raw Fisher
ctab=pd.crosstab(m.multi,m.bulge).values
od,pf=stats.fisher_exact(ctab)
print(f"  (raw Fisher: OR={od:.2f}, p={pf:.4f})")

# ---------- a_in vs single-Burkert a (capped, same machinery, seed 7) ----------
print("\nTEST 2 — a_in vs same-galaxy single-Burkert a (capped N=2 galaxies)")
rows=[]
for g in cap[cap.N_capped==2].galaxy:
    try: d=ts.load(g)
    except Exception: continue
    rng=np.random.default_rng(7); c=tc.best_tiers(d,rng); byN={z[2]:z for z in c}
    if 1 not in byN or 2 not in byN: continue
    a1=tc.unpack(byN[1][3],1,d['r'].min(),d['rmax'])[0][1]
    (p0i,ai),(p0o,ao)=tc.unpack(byN[2][3],2,d['r'].min(),d['rmax'])
    rows.append(dict(galaxy=g,a_single=a1,a_in=ai,a_out=ao,
                     r_in=a1/ai, between=float(ai<=a1<=ao)))
t=pd.DataFrame(rows)
t.to_csv("../ain_vs_burkert.csv",index=False)
print(f"  n={len(t)}")
print(f"  a_single / a_in: median={t.r_in.median():.2f}  16-84%: {t.r_in.quantile(.16):.2f}-{t.r_in.quantile(.84):.2f}")
print(f"  a_single between a_in and a_out: {int(t.between.sum())}/{len(t)} ({100*t.between.mean():.0f}%)")
print(f"  a_single ~ a_in (within factor 1.5): {int((t.r_in<1.5).sum())}/{len(t)}  -> ADDITIVE cases")
print(f"  a_single > 2x a_in:                  {int((t.r_in>2).sum())}/{len(t)}  -> REORGANIZED cases")
rho,pp=stats.spearmanr(t.a_single,t.a_in)
print(f"  corr(a_single, a_in): rho={rho:.2f} p={pp:.4f}")
