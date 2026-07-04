# Generic Program-2 refit on a BBarolo ringlog. Usage: <SPARC name> <ringfile> <D_barolo>
import sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
import tiered_spheres as ts, tiered_spheres_capped as tc
g, ringfile, D_bar = sys.argv[1], sys.argv[2], float(sys.argv[3])
cat=pd.read_csv("../data/raw/sparc_sample123.csv").set_index('Galaxy')
cap=pd.read_csv("../data/tiered_spheres_capped.csv").set_index('galaxy')
t=np.loadtxt(ringfile)
D_sp=float(cat.loc[g,'D'])
r=t[:,0]*(D_sp/D_bar); vc=t[:,2]; ev=np.full_like(vc,3.0)
sp=ts.load(g)
v2b=np.interp(r,sp['r'],sp['v2b'])
keep=(vc**2>v2b)&(r>0)&(vc>0)
d=dict(r=r[keep],vo=vc[keep],ev=ev[keep],v2b=v2b[keep],n=int(keep.sum()),rmax=float(r[keep].max()))
print(f"{g}: rings used {d['n']}/{len(r)}, rmax={d['rmax']:.1f} kpc | SPARC-based N={int(cap.loc[g,'N_capped'])}")
rng=np.random.default_rng(7); c=tc.best_tiers(d,rng)
for z in sorted(c,key=lambda q:q[2]):
    print(f"  N={z[2]}: BIC={z[0]:.1f} chi2={z[1]:.1f}")
best=c[0]
print(f"-> Barolo-curve selection: N={best[2]}  (dBIC over N=1: {[z[0] for z in c if z[2]==1][0]-best[0]:.1f})" if best[2]!=1 else f"-> Barolo-curve selection: N=1")
if best[2]==2:
    (p0i,ai),(p0o,ao)=tc.unpack(best[3],2,d['r'].min(),d['rmax'])
    rr=np.linspace(0.05,d['rmax'],2000)
    dd=ts.v2_burk(rr,p0o,ao)-ts.v2_burk(rr,p0i,ai)
    s=np.where(np.diff(np.sign(dd))!=0)[0]
    print(f"   r_x={rr[s[0]]:.2f} kpc, a_in={ai:.2f}, a_out={ao:.2f}" if len(s) else f"   no crossover; a_in={ai:.2f}, a_out={ao:.2f}")
