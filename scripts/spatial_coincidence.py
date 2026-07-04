# Convergent-validity: does the sphere CROSSOVER radius (where outer sphere overtakes inner)
# coincide with the INDEPENDENTLY-fit Gaussian shell radius? Test vs two nulls:
#   (1) randomized shell radii (permutation), (2) half-light radius (generic mid-disk scale).
# Spheres FROZEN (uncapped two_sphere_params.csv has p0/a for both); shells from sweep.
import numpy as np, pandas as pd
from scipy import stats
import tiered_spheres as ts

sp=pd.read_csv("../two_sphere_params.csv")          # galaxy, p0_in,a_in,p0_out,a_out
cat=pd.read_csv("../data/raw/sparc_sample123.csv")
shl=pd.read_csv("../data/processed/shell_model_sweep_shells.csv")
sh=shl[(shl.model=='burkert')&(np.isclose(shl.cap,0.4))&(shl.shell_idx>0)].copy()
sh['r_kpc']=pd.to_numeric(sh.r_kpc,errors='coerce')

def crossover(p0i,ai,p0o,ao,rmax):
    # radius where outer sphere's V-contribution overtakes inner's (within data)
    r=np.linspace(0.05,rmax,2000)
    vi=ts.v2_burk(r,p0i,ai); vo=ts.v2_burk(r,p0o,ao)
    d=vo-vi
    s=np.where(np.diff(np.sign(d))!=0)[0]
    return r[s[0]] if len(s) else np.nan

rows=[]
for _,x in sp.iterrows():
    g=x.galaxy
    d=ts.load(g); rc=crossover(x.p0_in,x.a_in,x.p0_out,x.a_out,d['rmax'])
    sg=sh[sh.galaxy==g]
    if len(sg)==0 or not np.isfinite(rc): continue
    # nearest shell radius to the crossover
    r_sh=sg.r_kpc.values
    nearest=r_sh[np.argmin(np.abs(r_sh-rc))]
    reff=cat.loc[cat.Galaxy==g,'Reff'].values
    rows.append(dict(galaxy=g,r_cross=rc,r_shell=nearest,rmax=d['rmax'],
                     reff=reff[0] if len(reff) else np.nan))
m=pd.DataFrame(rows).dropna(subset=['r_cross','r_shell'])
print(f"galaxies with both a sphere-crossover and a shell: {len(m)}")

# normalize offsets by rmax (so big & small galaxies comparable)
obs=np.abs(m.r_cross-m.r_shell)/m.rmax
print(f"\n--- |crossover - shell| / rmax ---")
print(f"  median fractional offset (sphere vs shell): {np.median(obs):.3f}")
# null 1: permuted shell radii
rng=np.random.default_rng(0); perm=[]
for _ in range(5000):
    sshuf=m.r_shell.sample(frac=1,random_state=rng.integers(1e9)).values
    perm.append(np.median(np.abs(m.r_cross.values-sshuf)/m.rmax.values))
perm=np.array(perm); p_perm=(perm<=np.median(obs)).mean()
print(f"  null (shuffled shells): median offset {np.median(perm):.3f}  | p(obs<=null)={p_perm:.4f}")
# null 2: half-light radius as the 'generic scale' competitor
off_reff=np.abs(m.r_cross-m.reff)/m.rmax
print(f"  crossover vs half-light radius offset: median {np.nanmedian(off_reff):.3f}")
# direct correlation crossover vs shell
r,p=stats.spearmanr(m.r_cross,m.r_shell)
print(f"\n--- do they co-locate? Spearman(r_cross, r_shell) = {r:.2f}  p={p:.4f} ---")
r2,p2=stats.spearmanr(m.r_cross,m.reff)
print(f"    (control) Spearman(r_cross, r_eff)   = {r2:.2f}  p={p2:.4f}")
m.to_csv("../spatial_coincidence.csv",index=False)
print("\nsaved spatial_coincidence.csv")
