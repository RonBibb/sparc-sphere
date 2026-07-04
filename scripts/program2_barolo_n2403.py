# PROGRAM 2 WINNER-SIDE TEST #1: NGC2403 via 3D-Barolo (authors' published config).
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
import tiered_spheres as ts, tiered_spheres_capped as tc

cat=pd.read_csv("../data/raw/sparc_sample123.csv").set_index('Galaxy')
cap=pd.read_csv("../data/tiered_spheres_capped.csv").set_index('galaxy')
g='NGC2403'
t=np.loadtxt("../program2/data/barolo_examples/examples/output/ngc2403/rings_final2.txt")
D_bar=3.2; D_sp=float(cat.loc[g,'D'])
r=t[:,0]*(D_sp/D_bar); vc=t[:,2]
# Barolo's ringlog has no per-ring Vrot error column in this version; use a
# conservative floor: max(2 km/s, half the ring-to-ring scatter of a 5pt spline resid)
ev=np.full_like(vc,3.0)
sp=ts.load(g)
v2b=np.interp(r,sp['r'],sp['v2b'])
keep=(vc**2>v2b)&(r>0)
d=dict(r=r[keep],vo=vc[keep],ev=ev[keep],v2b=v2b[keep],n=int(keep.sum()),rmax=float(r[keep].max()))
print(f"{g}: Barolo rings used {d['n']}/41, rmax={d['rmax']:.1f} kpc (SPARC rmax={cap.loc[g,'tier_rmax'] if 'tier_rmax' in cap.columns else 'n/a'})")
rng=np.random.default_rng(7); c=tc.best_tiers(d,rng)
byN={z[2]:z for z in c}
print(f"SPARC-based selection: N={int(cap.loc[g,'N_capped'])}")
print("Barolo-curve selection:")
for z in sorted(c,key=lambda q:q[2]):
    print(f"  N={z[2]}: BIC={z[0]:.1f} chi2={z[1]:.1f}")
best=c[0]
print(f"-> BIC-selected N={best[2]}")
if best[2]>=2:
    (p0i,ai),(p0o,ao)=tc.unpack(best[3],2,d['r'].min(),d['rmax'])
    rr=np.linspace(0.05,d['rmax'],2000)
    dd=ts.v2_burk(rr,p0o,ao)-ts.v2_burk(rr,p0i,ai)
    s=np.where(np.diff(np.sign(dd))!=0)[0]
    rx=rr[s[0]] if len(s) else np.nan
    print(f"   crossover r_x = {rx:.2f} kpc  (SPARC-based r_x ~ 2.3 kpc from MOM pilot)")
    print(f"   a_in={ai:.2f} a_out={ao:.2f} kpc")
