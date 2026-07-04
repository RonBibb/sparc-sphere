# DISCRIMINATOR #1, MASS-MATCHED: for each two-sphere host, build the clean rho0-scale
# locus from N=1 halos near the SAME Vflat, then measure where that host's inner and
# outer components fall relative to THAT local locus. Kills the mass-regime confound.
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from scipy import stats
cat=pd.read_csv("../data/raw/sparc_sample123.csv").set_index('Galaxy')
S=pd.read_csv("../data/single_burkert_all.csv")
TS=pd.read_csv("../data/two_sphere_params.csv")
S['vflat']=[cat.loc[g,'Vflat'] if g in cat.index else np.nan for g in S.galaxy]
TS['vflat']=[cat.loc[g,'Vflat'] if g in cat.index else np.nan for g in TS.galaxy]
clean=S[S.N==1].dropna(subset=['vflat']).reset_index(drop=True)
cx,cy,cv=clean['loga'].values,clean['logp0'].values,clean['vflat'].values

def local_locus(v, w0=20, nmin=10):
    w=w0
    while w<200:
        m=np.abs(cv-v)<=w
        if m.sum()>=nmin: break
        w+=10
    x,y=cx[m],cy[m]
    sl,ic,r,p,se=stats.linregress(x,y)
    sc=np.std(y-(sl*x+ic),ddof=2)
    return sl,ic,max(sc,0.05),int(m.sum()),w

rows=[]
for _,row in TS.iterrows():
    if not np.isfinite(row['vflat']): continue
    sl,ic,sc,nn,w=local_locus(row['vflat'])
    io=(row['p0_in']-(sl*np.log10(row['a_in'])+ic))/sc
    oo=(row['p0_out']-(sl*np.log10(row['a_out'])+ic))/sc
    rows.append(dict(galaxy=row['galaxy'],vflat=row['vflat'],n_local=nn,window=w,
                     in_off=io,out_off=oo))
R=pd.DataFrame(rows)
print(f"mass-matched offsets for {len(R)} two-sphere hosts (local clean locus each)")
print(f"  median local neighbors: {int(R.n_local.median())}, median window: {int(R.window.median())} km/s")
for tag,col in [("INNER",R.in_off),("OUTER",R.out_off)]:
    t=stats.ttest_1samp(col.dropna(),0)
    w=stats.wilcoxon(col.dropna())
    print(f"  {tag}: median {col.median():+.2f}s  mean {col.mean():+.2f}s  "
          f"|off|>2: {int((col.abs()>2).sum())}/{len(col)}  "
          f"t-test p={t.pvalue:.1e}  Wilcoxon p={w.pvalue:.1e}")
# direction summary
print(f"\ninner below relation (lower rho0 than mass-matched halos): {int((R.in_off<0).sum())}/{len(R)}")
print(f"outer below relation: {int((R.out_off<0).sum())}/{len(R)}")
R.to_csv("../data/scaling_massmatched.csv",index=False)
print("wrote scaling_massmatched.csv")
# biggest outliers (candidate debris)
print("\nmost displaced OUTER components (|off|, candidate non-halo):")
print(R.reindex(R.out_off.abs().sort_values(ascending=False).index)[['galaxy','vflat','out_off','in_off']].head(8).to_string(index=False))
