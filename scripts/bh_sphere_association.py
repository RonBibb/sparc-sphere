import numpy as np, pandas as pd, warnings
from scipy import stats
warnings.filterwarnings("ignore")
import tiered_spheres as ts

bh=pd.read_csv("../../sparc_mbh_dgc_catalog.csv")
print("MBH_method counts:"); print(bh.MBH_method.value_counts(dropna=False).to_string())
F=pd.read_csv("../data/forced_two_sphere.csv")
W=F[F.group=='winner'].copy()
cap=pd.read_csv("../data/tiered_spheres_capped.csv")
cat=pd.read_csv("../data/raw/sparc_sample123.csv")

# per-sphere enclosed masses within data range
W['M_in'] =[ts.M_burk(r,p,a) for r,p,a in zip(W.rmax,W.p0_in ,W.a_in )]
W['M_out']=[ts.M_burk(r,p,a) for r,p,a in zip(W.rmax,W.p0_out,W.a_out)]
W['M_tot']=W.M_in+W.M_out
W['f_in']=W.M_in/W.M_tot
m=W.merge(bh[['Galaxy','MBH','MBH_method']],left_on='galaxy',right_on='Galaxy')\
   .merge(cat[['Galaxy','Vflat']],on='Galaxy')
m=m.dropna(subset=['MBH'])
m['logMBH']=np.log10(m.MBH)
print(f"\nwinners with MBH: {len(m)}  (methods: {m.MBH_method.value_counts().to_dict()})")

print("\n--- RAW associations (EXPECT strong & circular: MBH=f(Vflat)) ---")
for col,lab in [('M_tot','total sphere mass'),('M_in','inner sphere'),('M_out','outer sphere')]:
    r,p=stats.spearmanr(m.logMBH,np.log10(m[col]))
    print(f"  logMBH vs {lab:18s}: rho={r:+.2f}  p={p:.1e}")

print("\n--- PARTITION test (the only non-circular axis) ---")
r,p=stats.spearmanr(m.logMBH,m.f_in)
print(f"  logMBH vs inner fraction f_in: raw rho={r:+.2f}  p={p:.3f}")
# partial at fixed Vflat
z=np.log10(m.Vflat.values)
res=lambda y: y-np.polyval(np.polyfit(z,y,1),z)
rp,pp=stats.spearmanr(res(m.logMBH.values),res(m.f_in.values))
print(f"  partial (control Vflat):       rho={rp:+.2f}  p={pp:.3f}")
# sanity: how deterministic is MBH given Vflat in this catalog?
rv,pv=stats.spearmanr(m.logMBH,np.log10(m.Vflat))
print(f"  (circularity check: logMBH vs logVflat rho={rv:.2f} -> if ~1, partial is meaningless)")
# measured-MBH subset if any
meas=m[~m.MBH_method.astype(str).str.contains('DGC|n/a',case=False,na=False)]
print(f"\n  literature/measured-MBH subset among winners: n={len(meas)}")
if len(meas)>=5:
    r,p=stats.spearmanr(meas.logMBH,meas.f_in); print(f"  measured subset: logMBH vs f_in rho={r:+.2f} p={p:.3f}")
m[['galaxy','MBH','MBH_method','M_in','M_out','f_in','Vflat']].to_csv("../data/bh_sphere_association.csv",index=False)
print("\nsaved data/bh_sphere_association.csv")
