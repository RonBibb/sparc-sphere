import numpy as np, pandas as pd, warnings
from scipy import stats
warnings.filterwarnings("ignore")
import tiered_spheres as ts, tiered_spheres_capped as tc

m=pd.read_csv("../data/vdb16_sparc_matches.csv")
F=pd.read_csv("../data/forced_two_sphere.csv")
borderline=set(F[(F.group=='forced')&(F.dchi2>2)].galaxy)
cat=pd.read_csv("../data/raw/sparc_sample123.csv")

print(f"{'galaxy':10s} {'class':18s} {'logMBH':>7s} {'±':>5s} {'UL?':>4s}")
rows=[]
for _,r in m.iterrows():
    cls='winner' if r.N_capped>=2 else ('borderline' if r.galaxy in borderline else 'clean_single')
    ul=bool(r.UPPERLIMIT) if 'UPPERLIMIT' in r else False
    print(f"{r.galaxy:10s} {cls:18s} {r.MBH:7.2f} {r.DMBH:5.2f} {str(ul):>4s}")
    # fitted DM mass within data (N from selection)
    try: d=ts.load(r.galaxy)
    except Exception: continue
    rng=np.random.default_rng(7); c=tc.best_tiers(d,rng); byN={z[2]:z for z in c}
    N=int(r.N_capped); th=byN[N][3]
    Mdm=sum(ts.M_burk(d['rmax'],p0,a) for p0,a in tc.unpack(th,N,d['r'].min(),d['rmax']))
    vf=cat.loc[cat.Galaxy==r.galaxy,'Vflat'].values
    rows.append(dict(galaxy=r.galaxy,cls=cls,logMBH=r.MBH,dMBH=r.DMBH,ul=ul,
                     logMdm=np.log10(Mdm),Vflat=vf[0] if len(vf) else np.nan))
b=pd.DataFrame(rows); b.to_csv("../data/vdb16_baseline.csv",index=False)

print("\n=== BASELINE: clean singles, measured logMBH vs fitted DM mass ===")
cs=b[(b.cls=='clean_single')&(~b.ul)]
print(f"clean singles with real measurements (no upper limits): n={len(cs)}")
if len(cs)>=5:
    r1,p1=stats.spearmanr(cs.logMBH,cs.logMdm)
    r2,p2=stats.spearmanr(cs.logMBH,np.log10(cs.Vflat))
    print(f"  logMBH vs logM_DM(fitted): rho={r1:+.2f}  p={p1:.3f}")
    print(f"  logMBH vs logVflat:        rho={r2:+.2f}  p={p2:.3f}")
print("\nall matched, sorted:")
print(b.sort_values(['cls','logMBH']).to_string(index=False))
