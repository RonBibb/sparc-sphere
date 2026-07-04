# GEOMETRIC DISCRIMINATOR #1: scaling-relation membership.
# Q: do two-sphere COMPONENTS fall on the same rho0-scale relation that clean
#    single halos follow (=anchored secondary halos), or OFF it (=debris)?
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from scipy.optimize import least_squares
from scipy import stats
import tiered_spheres as ts
G=4.30091e-6

def fit_single(d):
    def resid(th):
        v2=d['v2b']+np.clip(ts.v2_burk(d['r'],th[0],th[1]),0,None)
        return (np.sqrt(v2)-d['vo'])/d['ev']
    best=None
    rng=np.random.default_rng(7)
    for _ in range(16):
        x0=[rng.uniform(6,9),rng.uniform(0.5,max(1.0,0.3*d['rmax']))]
        try: r=least_squares(resid,x0,bounds=([4,0.05],[10.5,max(2,d['rmax'])]),max_nfev=4000)
        except Exception: continue
        c=float(np.sum(r.fun**2))
        if best is None or c<best[0]: best=(c,r.x)
    return best[1] if best else None

cap=pd.read_csv("../data/tiered_spheres_capped.csv").set_index('galaxy')
rows=[]
for g in cap.index:
    try: d=ts.load(g)
    except Exception: continue
    if d['n']<6: continue
    p=fit_single(d)
    if p is None: continue
    rows.append(dict(galaxy=g,N=int(cap.loc[g,'N_capped']),logp0=p[0],a=p[1],
                     loga=np.log10(p[1]),rmax=d['rmax']))
S=pd.DataFrame(rows)
clean=S[S.N==1].copy()
print(f"single-Burkert fits: {len(S)} galaxies | clean N=1 locus: {len(clean)}")

# clean-halo locus in (log a, log rho0)
x=clean['loga'].values; y=clean['logp0'].values
sl,ic,r,p,se=stats.linregress(x,y)
resid_std=np.std(y-(sl*x+ic))
print(f"CLEAN LOCUS: logp0 = {sl:.3f}*loga + {ic:.3f}  (Spearman rho={stats.spearmanr(x,y)[0]:+.2f}, p={p:.1e}, scatter={resid_std:.3f} dex)")

# two-sphere components: how far off the locus (in dex, normalized by clean scatter)?
TS=pd.read_csv("../data/two_sphere_params.csv")
def offset(loga,logp0): return (logp0-(sl*loga+ic))/resid_std
TS['in_off']=offset(np.log10(TS.a_in),TS.p0_in)
TS['out_off']=offset(np.log10(TS.a_out),TS.p0_out)
print(f"\nINNER components: median offset {TS.in_off.median():+.2f} sigma_clean, "
      f"|off|>2: {(TS.in_off.abs()>2).sum()}/{len(TS)}")
print(f"OUTER components: median offset {TS.out_off.median():+.2f} sigma_clean, "
      f"|off|>2: {(TS.out_off.abs()>2).sum()}/{len(TS)}")
# formal: are inner/outer offsets consistent with clean scatter (KS vs N(0,1))?
for tag,col in [("inner",TS.in_off),("outer",TS.out_off)]:
    ks=stats.kstest(col.dropna(),'norm')
    print(f"  {tag}: KS vs clean-normal p={ks.pvalue:.1e}  (small p = off-relation)")
S.to_csv("../data/single_burkert_all.csv",index=False)
TS.to_csv("../data/scaling_offsets.csv",index=False)
print("\nwrote single_burkert_all.csv, scaling_offsets.csv")
