# RESIDUAL-a SECOND-PARAMETER HUNT
# Q: the single-domain core radius 'a' is ~independent of M_halo (r=0.05) and scatters ~2x.
#    What does the residual a (at fixed M_halo) correlate with? Each hypothesis -> a prediction:
#    H1 distributed-SBH/bias  -> central/bulge proxies (bulge frac, central concentration)
#    H2 hidden multi-shell/BIC -> DATA QUALITY (n_points, Q, rmax coverage) [poorer data -> more scatter]
#    H3 age/assembly           -> surface brightness, T-type, M*/Mhalo (DC14 feedback-coring)
#    H4 framework wrong/baryonic-> tracks baryonic proxies cleanly, nothing central
#    H5 hidden complexity      -> correlates with NOTHING measurable
import pandas as pd, numpy as np, warnings
warnings.filterwarnings("ignore")
from scipy import stats
S=pd.read_csv("data/single_burkert_all.csv")
cat=pd.read_csv("data/raw/sparc_sample123.csv").set_index('Galaxy')

pure=S[S.N==1].dropna(subset=['logp0','loga']).copy().set_index('galaxy')
# join proxies
for c in ['T','L36','Reff','SBeff','Rdisk','SBdisk','MHI','RHI','Vflat','Q',
          'M_star','M_halo','logM_star','logM_halo','logM_halo_per_star','D','Inc']:
    pure[c]=[cat.loc[g,c] if g in cat.index else np.nan for g in pure.index]
pure['n']=S.set_index('galaxy').loc[pure.index,'rmax'] if False else np.nan
# get n_points & rmax from the fit file
pure['rmax']=S.set_index('galaxy').loc[pure.index,'rmax']
# derived proxies
pure['logMHI']=np.log10(pure['MHI'].clip(lower=1))
pure['gasfrac']=pure['MHI']/(pure['M_star']+pure['MHI'])      # gas richness
pure['MHI_Mstar']=pure['MHI']/pure['M_star']
pure['rmax_over_a']=pure['rmax']/(10**pure['loga'])           # coverage in core units
pure['SB_central']=pure['SBdisk']                              # disk central SB proxy

# RESIDUAL a at fixed M_halo: regress loga on logM_halo, take residual
d=pure.dropna(subset=['loga','logM_halo']).copy()
sl,ic,r,p,se=stats.linregress(d.logM_halo,d.loga)
d['res_a']=d.loga-(sl*d.logM_halo+ic)
print(f"baseline: loga vs logM_halo  r={r:+.3f} (mass barely predicts a)")
print(f"residual-a sample: N={len(d)}, scatter {d.res_a.std():.3f} dex\n")

proxies={
 'logM_halo_per_star (DC14)':'logM_halo_per_star',
 'M*/Mhalo inverse':'logM_star',
 'SBeff (surf bright)':'SBeff',
 'SBdisk':'SBdisk',
 'T-type (morph/age)':'T',
 'gas fraction':'gasfrac',
 'logMHI':'logMHI',
 'Reff':'Reff',
 'Rdisk':'Rdisk',
 'Vflat':'Vflat',
 'logL36':'L36',
 'rmax coverage (DATA)':'rmax',
 'rmax/a coverage (DATA)':'rmax_over_a',
 'Q quality (DATA)':'Q',
 'Inc':'Inc',
}
print(f"{'proxy':28} {'hypothesis':6} {'r':>7} {'p':>9} {'n':>4}")
print("-"*62)
results=[]
hyp={'logM_halo_per_star':'H3','logM_star':'H3','SBeff':'H3','SBdisk':'H3','T':'H3',
     'gasfrac':'H4','logMHI':'H4','Reff':'H4','Rdisk':'H4','Vflat':'H4','L36':'H4',
     'rmax':'H2','rmax_over_a':'H2','Q':'H2','Inc':'??'}
for name,col in proxies.items():
    dd=d.dropna(subset=['res_a',col])
    if len(dd)<10: continue
    x=dd[col].values
    if col in ('L36','gasfrac','MHI_Mstar'): x=np.log10(np.clip(x,1e-6,None))
    rr,pp=stats.pearsonr(dd.res_a,x)
    results.append((name,hyp.get(col,'?'),rr,pp,len(dd)))
    flag=' ***' if pp<0.01 else (' *' if pp<0.05 else '')
    print(f"{name:28} {hyp.get(col,'?'):6} {rr:+7.3f} {pp:9.1e} {len(dd):4d}{flag}")

# multivariate: which proxies SURVIVE together?
print("\n=== multivariate (significant proxies, standardized) ===")
sig=[c for n,c in proxies.items() if c in d and stats.pearsonr(*[d.dropna(subset=['res_a',c])[k] for k in ('res_a',c)])[1]<0.05 and d[c].notna().sum()>10]
sig=list(dict.fromkeys(sig))
dd=d.dropna(subset=['res_a']+sig).copy()
if len(sig)>=2 and len(dd)>len(sig)+5:
    X=np.column_stack([(dd[c]-dd[c].mean())/dd[c].std() for c in sig]+[np.ones(len(dd))])
    co,*_=np.linalg.lstsq(X,dd.res_a.values,rcond=None)
    pred=X@co; r2=1-np.sum((dd.res_a-pred)**2)/np.sum((dd.res_a-dd.res_a.mean())**2)
    print(f"  proxies: {sig}")
    print(f"  standardized coefs: {[f'{c:+.3f}' for c in co[:-1]]}")
    print(f"  joint R^2={r2:.3f} (N={len(dd)})")
else:
    print(f"  <2 significant proxies or too few points; sig={sig}")
d.to_csv("data/residual_a_proxies.csv")
