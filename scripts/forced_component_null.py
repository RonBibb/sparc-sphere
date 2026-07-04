# FORCED-COMPONENT NULL for discriminator #1.
# Q: is the inner-component "below-relation" offset (~ -0.8 sigma) a PHYSICAL property of
#    genuine two-domain galaxies, or a generic ARTIFACT of forcing a 2-sphere fit?
# Method: run the IDENTICAL mass-matched local-locus offset procedure on the FORCED
#    two-sphere fits of single-domain (N=1) galaxies, compare to the genuine WINNERS.
# Fork:
#   forced inner ALSO ~ -0.8s  -> artifact of fitting regime -> physical interp DIES.
#   forced inner ~ 0 (symmetric) -> the winner signal is specific to real 2-domain -> SURVIVES.
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from scipy import stats
cat=pd.read_csv("../data/raw/sparc_sample123.csv").set_index('Galaxy')
S=pd.read_csv("../data/single_burkert_all.csv")
F=pd.read_csv("../data/forced_two_sphere.csv")
S['vflat']=[cat.loc[g,'Vflat'] if g in cat.index else np.nan for g in S.galaxy]
F['vflat']=[cat.loc[g,'Vflat'] if g in cat.index else np.nan for g in F.galaxy]

# SAME clean locus as the real test: N=1 single-Burkert halos
clean=S[S.N==1].dropna(subset=['vflat']).reset_index(drop=True)
cx,cy,cv=clean['loga'].values,clean['logp0'].values,clean['vflat'].values
def local_locus(v,w0=20,nmin=10):
    w=w0
    while w<200:
        m=np.abs(cv-v)<=w
        if m.sum()>=nmin: break
        w+=10
    x,y=cx[m],cy[m]; sl,ic,r,p,se=stats.linregress(x,y)
    sc=np.std(y-(sl*x+ic),ddof=2)
    return sl,ic,max(sc,0.05),int(m.sum()),w

# QUALITY GATE: exclude degenerate forced fits.
#  - drop railed at 5.0 (hit the separation bound) -> components not independently constrained
#  - ratio > 30 (extreme scale split) -> one component pushed to a bound
#  - a_in or a_out at param bounds
def offsets(df,label):
    rows=[]; n_excl=0
    for _,row in df.iterrows():
        if not np.isfinite(row['vflat']): continue
        # quality gate (only meaningful for forced; winners kept as-is but same gate applied for fairness)
        railed = (abs(row['drop']-5.0)<1e-3) or (row['ratio']>30) or (row['a_in']<0.12) or (row['p0_in']>9.9) or (row['p0_out']<1.7)
        if railed:
            n_excl+=1; continue
        sl,ic,sc,nn,w=local_locus(row['vflat'])
        io=(row['p0_in']-(sl*np.log10(row['a_in'])+ic))/sc
        oo=(row['p0_out']-(sl*np.log10(row['a_out'])+ic))/sc
        rows.append(dict(galaxy=row['galaxy'],group=label,vflat=row['vflat'],in_off=io,out_off=oo))
    return pd.DataFrame(rows),n_excl

forced=F[F.group=='forced']
winner=F[F.group=='winner']
print(f"forced N=1 galaxies: {len(forced)}, genuine winners: {len(winner)}")

RF,ef=offsets(forced,'forced')
RW,ew=offsets(winner,'winner')
print(f"after quality gate: forced {len(RF)} (excluded {ef} railed), winner {len(RW)} (excluded {ew})\n")

def summ(R,tag):
    for nm,col in [("INNER",R.in_off),("OUTER",R.out_off)]:
        c=col.dropna()
        t=stats.ttest_1samp(c,0)
        print(f"  [{tag}] {nm}: median {c.median():+.2f}s  mean {c.mean():+.2f}s  "
              f"below: {int((c<0).sum())}/{len(c)}  t-test vs 0: p={t.pvalue:.2e}")
print("=== GENUINE WINNERS (reference) ===");      summ(RW,"win")
print("=== FORCED N=1 (the null) ===");            summ(RF,"forced")

# direct two-sample: do forced inner offsets differ from winner inner offsets?
print("\n=== FORK TEST: forced-inner vs winner-inner ===")
mw=stats.mannwhitneyu(RF.in_off.dropna(),RW.in_off.dropna())
print(f"  Mann-Whitney forced-inner vs winner-inner: p={mw.pvalue:.2e}")
ks=stats.ks_2samp(RF.in_off.dropna(),RW.in_off.dropna())
print(f"  KS forced-inner vs winner-inner: p={ks.pvalue:.2e}")
print(f"\n  winner inner median: {RW.in_off.median():+.2f}s")
print(f"  forced inner median: {RF.in_off.median():+.2f}s")
verdict = ("ARTIFACT: forced inner reproduces winner offset -> physical interp WEAKENED"
           if RF.in_off.median()<-0.4 and mw.pvalue>0.05 else
           "SURVIVES: forced inner differs from winner -> winner signal is specific/physical"
           if mw.pvalue<0.05 else "AMBIGUOUS")
print(f"\n  >>> {verdict}")
out=pd.concat([RW,RF]); out.to_csv("../data/forced_component_null.csv",index=False)
print("\nwrote forced_component_null.csv")
