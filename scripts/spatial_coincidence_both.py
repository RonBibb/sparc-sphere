# Same crossover-vs-shell null test, run for BOTH uncapped and capped sphere fits.
import numpy as np, pandas as pd
from scipy import stats
import tiered_spheres as ts

cat=pd.read_csv("../data/raw/sparc_sample123.csv")
shl=pd.read_csv("../data/processed/shell_model_sweep_shells.csv")
sh=shl[(shl.model=='burkert')&(np.isclose(shl.cap,0.4))&(shl.shell_idx>0)].copy()
sh['r_kpc']=pd.to_numeric(sh.r_kpc,errors='coerce')

def crossover(p0i,ai,p0o,ao,rmax):
    r=np.linspace(0.05,rmax,2000)
    d=ts.v2_burk(r,p0o,ao)-ts.v2_burk(r,p0i,ai)
    s=np.where(np.diff(np.sign(d))!=0)[0]
    return r[s[0]] if len(s) else np.nan

def run(sp_df, label, get_params):
    rows=[]
    for _,x in sp_df.iterrows():
        g=x.galaxy
        try: d=ts.load(g)
        except Exception: continue
        p0i,ai,p0o,ao=get_params(x)
        rc=crossover(p0i,ai,p0o,ao,d['rmax'])
        sg=sh[sh.galaxy==g]
        if len(sg)==0 or not np.isfinite(rc): continue
        r_sh=sg.r_kpc.values; nearest=r_sh[np.argmin(np.abs(r_sh-rc))]
        rows.append(dict(galaxy=g,r_cross=rc,r_shell=nearest,rmax=d['rmax']))
    m=pd.DataFrame(rows).dropna()
    obs=np.median(np.abs(m.r_cross-m.r_shell)/m.rmax)
    rng=np.random.default_rng(0)
    perm=np.array([np.median(np.abs(m.r_cross.values-m.r_shell.sample(frac=1,random_state=rng.integers(1e9)).values)/m.rmax.values) for _ in range(5000)])
    p_perm=(perm<=obs).mean()
    rho,p=stats.spearmanr(m.r_cross,m.r_shell)
    print(f"\n===== {label}  (n={len(m)}) =====")
    print(f"  Spearman(r_cross, r_shell) = {rho:.2f}  p={p:.4f}")
    print(f"  median frac offset = {obs:.3f}   shuffle-null median = {np.median(perm):.3f}   p(obs<=null) = {p_perm:.4f}")
    return m

# UNCAPPED: two_sphere_params.csv has p0_in,a_in,p0_out,a_out
up=pd.read_csv("../two_sphere_params.csv")
run(up,"UNCAPPED spheres", lambda x:(x.p0_in,x.a_in,x.p0_out,x.a_out))

# CAPPED: tiered_spheres_capped.csv has only tier_a (a1;a2), NOT rho0.
# Recover rho0 per capped sphere by re-reading... we only have a. Need p0. 
# The capped run didn't save p0. Reconstruct via the capped fitter (frozen seed) -> get full theta.
import tiered_spheres_capped as tc
cap=pd.read_csv("../data/processed/tiered_spheres_capped.csv")
cap2=cap[cap.N_capped==2]
rows=[]
for _,x in cap2.iterrows():
    g=x.galaxy
    try: d=ts.load(g)
    except Exception: continue
    rng=np.random.default_rng(7); c=tc.best_tiers(d,rng); byN={z[2]:z for z in c}
    if 2 not in byN: continue
    th=byN[2][3]; comps=tc.unpack(th,2,d['r'].min(),d['rmax'])
    (p0i,ai),(p0o,ao)=comps
    rows.append(dict(galaxy=g,p0_in=p0i,a_in=ai,p0_out=p0o,a_out=ao))
capp=pd.DataFrame(rows)
run(capp,"CAPPED spheres", lambda x:(x.p0_in,x.a_in,x.p0_out,x.a_out))
