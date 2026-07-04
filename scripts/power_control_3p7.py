# POWER-CONTROL for the 3 deferred galaxies (3.7) — injection-recovery, CORRECTED.
# The detectable "feature" = residual of the TRUE two-domain curve vs its best SINGLE-domain
# fit (the actual signal BIC must find), NOT the inner component's full velocity.
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from scipy.optimize import least_squares
import tiered_spheres as ts
G=ts.G
def M_burk(r,p0,a):
    rho=10**p0; a=max(a,1e-6)
    return np.pi*rho*a**3*(np.log(1+r**2/a**2)+2*np.log(1+r/a)-2*np.arctan(r/a))
def v2_1(r,p0,a): return np.maximum(G*M_burk(r,p0,a)/np.maximum(r,1e-6),0)
def v2_2(r,p0i,ai,p0o,ao): return v2_1(r,p0i,ai)+v2_1(r,p0o,ao)
def fit1(r,v,e):
    def res(t): return (np.sqrt(np.clip(v2_1(r,t[0],t[1]),0,None))-v)/e
    best=None
    for _ in range(15):
        x0=[np.random.uniform(6,9),np.random.uniform(0.5,0.3*r.max())]
        try: rr=least_squares(res,x0,bounds=([3,0.1],[10,r.max()*1.5]),max_nfev=4000)
        except: continue
        c=np.sum(res(rr.x)**2)
        if best is None or c<best[0]: best=(c,rr.x)
    return best
def fit2(r,v,e):
    def res(t):
        p0i,ai,dp,la=t
        return (np.sqrt(np.clip(v2_2(r,p0i,ai,p0i-dp,ai*10**la),0,None))-v)/e
    best=None
    for _ in range(25):
        x0=[np.random.uniform(7,9),np.random.uniform(0.3,0.15*r.max()),
            np.random.uniform(0.3,1.5),np.random.uniform(0.2,0.8)]
        try: rr=least_squares(res,x0,bounds=([3,0.1,0.05,0.05],[10,r.max(),5,1.5]),max_nfev=5000)
        except: continue
        c=np.sum(res(rr.x)**2)
        if best is None or c<best[0]: best=(c,rr.x)
    return best
def dBIC(r,v,e):
    n=len(r); b1=fit1(r,v,e); b2=fit2(r,v,e)
    if not b1 or not b2: return None
    return (b1[0]+2*np.log(n))-(b2[0]+4*np.log(n))

TP=pd.read_csv("../data/two_sphere_params.csv").set_index('galaxy')
cat=pd.read_csv("../data/raw/sparc_sample123.csv").set_index('Galaxy')
curves={'NGC2841':"../program2/data/things_cubes/out_NGC_2841/NGC2841H_2drings.txt",
 'NGC3521':"../program2/data/things_cubes/out_NGC_3521/NGC3521H_2drings.txt",
 'NGC1003':"../program2/data/halogas_cubes/out_NGC1003_deep/ngc1003_2drings.txt"}
def load_curve(g,path):
    D=cat.loc[g,'D']; kpc_as=D*1e3*np.pi/180/3600; rows=[]
    for ln in open(path):
        if ln.startswith('#'): continue
        p=ln.split()
        if len(p)<4: continue
        try:
            ras=float(p[1]); vrot=float(p[3])
            if np.isfinite(ras) and np.isfinite(vrot) and vrot>0: rows.append((ras*kpc_as,vrot))
        except: continue
    a=np.array(rows); return a[:,0],a[:,1]

print(f"{'galaxy':9} {'n':>4} {'rmax':>6} {'feat_resid':>10} {'floor':>7} {'med_err':>8} {'VERDICT':>26}")
print("-"*80); out=[]; np.random.seed(7)
for g,path in curves.items():
    r,v=load_curve(g,path)
    if len(r)<6: print(f"{g}: too few rings"); continue
    e=np.maximum(3.0,0.03*v)
    pr=TP.loc[g]
    # TRUE two-domain curve sampled at this galaxy's radii (SPARC params)
    v_true=np.sqrt(np.clip(v2_2(r,pr.p0_in,pr.a_in,pr.p0_out,pr.a_out),0,None))
    # best single-domain fit to that true curve -> residual = the detectable feature
    b1t=fit1(r,v_true,e); v1=np.sqrt(np.clip(v2_1(r,b1t[1][0],b1t[1][1]),0,None))
    feat=v_true-v1
    feat_amp=np.max(np.abs(feat))            # peak detectable deviation (km/s)
    # injection-recovery on the REAL independent curve's smooth baseline + scaled feature
    b1=fit1(r,v,e); base=np.sqrt(np.clip(v2_1(r,b1[1][0],b1[1][1]),0,None))
    floor=None
    for A in np.linspace(0.3,4.0,38):
        recovered=0
        for trial in range(8):  # average over noise realizations
            vinj=base+A*feat+np.random.normal(0,e)
            db=dBIC(r,vinj,e)
            if db and db>6: recovered+=1
        if recovered>=6:  # detected in >=75% of noise realizations
            floor=A*feat_amp; break
    med_err=np.median(e)
    detectable=(floor is not None) and (feat_amp>=floor)
    verdict="DETECTABLE" if detectable else ("BELOW FLOOR (uninform.)" if floor else "undetectable@4x")
    fstr=f"{floor:.1f}" if floor else ">{:.0f}".format(4*feat_amp)
    print(f"{g:9} {len(r):4d} {r.max():6.1f} {feat_amp:10.1f} {fstr:>7} {med_err:8.1f} {verdict:>26}")
    out.append(dict(galaxy=g,n=len(r),rmax_kpc=round(r.max(),1),feat_resid_kms=round(feat_amp,1),
                    detect_floor_kms=round(floor,1) if floor else None,med_err_kms=round(med_err,1),
                    uninformative=not detectable))
pd.DataFrame(out).to_csv("../data/power_control_3p7.csv",index=False)
print("\nfeat_resid = peak deviation the two-domain feature adds over best single fit (the signal)")
print("floor = injected feature amplitude BIC recovers in >=75% of noise realizations")
print("uninformative where feat_resid < floor: curve cannot detect the real feature.")
