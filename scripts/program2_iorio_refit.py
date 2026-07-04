# PROGRAM 2 FIRST REFIT: Iorio+2017 (3D-Barolo, L1-independent) curves vs SPARC-based fits.
# For each overlap galaxy: Vobs := Iorio Vc (radii rescaled to SPARC distance),
# baryons := SPARC rotmod interpolated onto Iorio grid, fitter := capped, seed 7, UNCHANGED.
# Compare BIC-selected N against the SPARC-based N_capped.
import os, re, glob, numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
import tiered_spheres as ts, tiered_spheres_capped as tc

IOR="../program2/data/iorio2017/finalrot"
cap=pd.read_csv("../data/tiered_spheres_capped.csv").set_index('galaxy')
cat=pd.read_csv("../data/raw/sparc_sample123.csv").set_index('Galaxy')

def sparc_name(stem):
    m=re.match(r'(ddo|ngc|ugc)(\d+)',stem)
    if m:
        pre=m.group(1).upper(); num=m.group(2)
        if pre=='DDO': return f"DDO{int(num):03d}"
        if pre=='NGC': return f"NGC{int(num):04d}"
        if pre=='UGC': return f"UGC{int(num):05d}"
    return {'wlm':'WLM','cvidwa':'CVnIdwA'}.get(stem,stem.upper())

rows=[]
for f in sorted(glob.glob(f"{IOR}/*_onlinetab.txt")):
    stem=os.path.basename(f).replace('_onlinetab.txt','')
    g=sparc_name(stem)
    if g not in cap.index: continue
    hdr=open(f).read(400)
    D_ior=float(re.search(r'Distance:\s*([\d.]+)',hdr).group(1))
    D_sp=float(cat.loc[g,'D'])
    t=np.loadtxt(f)
    r=t[:,1]*(D_sp/D_ior); vc=t[:,6]; ev=np.maximum(t[:,7],1.0)
    # SPARC baryons interpolated onto this grid
    sp=ts.load(g)
    v2b=np.interp(r,sp['r'],sp['v2b'])
    keep=(vc**2>v2b)&(r>0)
    if keep.sum()<6:
        rows.append(dict(galaxy=g,n_pts=int(keep.sum()),N_sparc=int(cap.loc[g,'N_capped']),N_iorio=-1,note='too few pts')); continue
    d=dict(r=r[keep],vo=vc[keep],ev=ev[keep],v2b=v2b[keep],n=int(keep.sum()),rmax=float(r[keep].max()))
    rng=np.random.default_rng(7); c=tc.best_tiers(d,rng)
    if not c:
        rows.append(dict(galaxy=g,n_pts=d['n'],N_sparc=int(cap.loc[g,'N_capped']),N_iorio=-1,note='fit failed')); continue
    bic,chi2,N=c[0][0],c[0][1],c[0][2]
    rows.append(dict(galaxy=g,n_pts=d['n'],D_ratio=round(D_sp/D_ior,3),
        N_sparc=int(cap.loc[g,'N_capped']),N_iorio=N,
        chi2red=round(chi2/max(1,d['n']-2*N),2),agree=int(N==int(cap.loc[g,'N_capped'])),note=''))
res=pd.DataFrame(rows)
res.to_csv("../program2/data/iorio_refit_results.csv",index=False)
print(res.to_string(index=False))
ok=res[res.N_iorio>=0]
print(f"\noverlap fit: {len(ok)}  |  N agrees with SPARC-based: {ok.agree.sum()}/{len(ok)}")
print(f"controls staying N=1 on independent curves: {((ok.N_sparc==1)&(ok.N_iorio==1)).sum()}/{(ok.N_sparc==1).sum()}")
