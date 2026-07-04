# Direct two-domain test on Sellwood WARP-AWARE DiskFit curves for NGC2841 & NGC3521.
# These were 'deferred/instrument-limited' — but the power test showed their features ARE
# detectable, so the honest move is to test the warp-aware curve directly: does BIC select
# N>=2 on Sellwood's curve? Positive -> reproduce. Negative -> real non-reproduction.
import numpy as np, pandas as pd, warnings, re
warnings.filterwarnings("ignore")
from scipy.optimize import least_squares
import tiered_spheres as ts
G=ts.G
def M_burk(r,p0,a):
    rho=10**p0; a=max(a,1e-6)
    return np.pi*rho*a**3*(np.log(1+r**2/a**2)+2*np.log(1+r/a)-2*np.arctan(r/a))
def v2_1(r,p0,a): return np.maximum(G*M_burk(r,p0,a)/np.maximum(r,1e-6),0)
def v2_2(r,t): return v2_1(r,t[0],t[1])+v2_1(r,t[0]-t[2],t[1]*10**t[3])
def fit(r,v,e,two):
    f=(lambda t:(np.sqrt(np.clip(v2_2(r,t),0,None))-v)/e) if two else (lambda t:(np.sqrt(np.clip(v2_1(r,t[0],t[1]),0,None))-v)/e)
    lo,hi=([3,0.1,0.05,0.05],[10,r.max(),5,1.5]) if two else ([3,0.1],[10,r.max()*1.5])
    best=None
    for _ in range(25):
        if two: x0=[np.random.uniform(7,9),np.random.uniform(0.3,0.15*r.max()),np.random.uniform(0.3,1.5),np.random.uniform(0.2,0.8)]
        else: x0=[np.random.uniform(6,9),np.random.uniform(0.5,0.3*r.max())]
        try: rr=least_squares(f,x0,bounds=(lo,hi),max_nfev=5000)
        except: continue
        c=np.sum(f(rr.x)**2)
        if best is None or c<best[0]: best=(c,rr.x)
    return best
cat=pd.read_csv("../data/raw/sparc_sample123.csv").set_index('Galaxy')
def sellwood_curve(fn,D):
    # parse Vt (circular rotation) vs radius(pix), convert pix->kpc. pixscale 1.5"/pix
    txt=open(fn).read(); px=1.5; kpc_as=D*1e3*np.pi/180/3600
    rows=[]; inb=False
    for ln in txt.splitlines():
        if ln.strip().startswith('r ') and 'Vt' in ln: inb=True; continue
        if inb:
            p=ln.split()
            if len(p)>=4 and re.match(r'^[\d.]+$',p[0]):
                try:
                    rpix=float(p[0]); Vt=float(p[2]); eVt=float(p[3])
                    if Vt>0: rows.append((rpix*px*kpc_as,Vt,max(eVt,3.0)))
                except: pass
    a=np.array(rows); return a[:,0],a[:,1],a[:,2]
np.random.seed(7)
print(f"{'galaxy':9} {'n':>4} {'rmax':>6} {'chi2_1':>8} {'chi2_2':>8} {'dBIC':>7} {'VERDICT':>18}")
print("-"*70)
for g,fn in [('NGC2841','/Users/ronbibb/Downloads/DiskFit_Sellwood/N2841.out'),
             ('NGC3521','/Users/ronbibb/Downloads/DiskFit_Sellwood/N3521.out')]:
    D=cat.loc[g,'D']; r,v,e=sellwood_curve(fn,D)
    # baryon subtraction: use SPARC rotmod baryon model interpolated
    d=ts.load(g)
    v2b=np.interp(r,d['r'],d['v2b'],left=d['v2b'][0],right=d['v2b'][-1])
    vdm=np.sqrt(np.clip(v**2-v2b,1,None))  # dark-matter-only velocity
    b1=fit(r,vdm,e,False); b2=fit(r,vdm,e,True)
    n=len(r); bic1=b1[0]+2*np.log(n); bic2=b2[0]+4*np.log(n); db=bic1-bic2
    verdict="REPRODUCES(N=2)" if db>6 else ("marginal" if db>0 else "single-domain")
    print(f"{g:9} {n:4d} {r.max():6.1f} {b1[0]:8.1f} {b2[0]:8.1f} {db:7.1f} {verdict:>18}")
