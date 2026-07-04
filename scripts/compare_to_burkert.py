import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import tiered_spheres as ts

gals=["NGC2841","NGC2403","NGC3521","NGC5055","NGC6946"]
sweep=pd.read_csv("../data/processed/shell_model_sweep_summary.csv")
rng=np.random.default_rng(7)
rows=[]
for g in gals:
    d=ts.load(g)
    cands=ts.best_tiers(d,4,20,rng)
    byN={c[2]:c for c in cands}
    bic1,chi1,_,_=byN[1]                       # single Burkert (1 concentric sphere)
    bicT,chiT,NT,_=cands[0]                     # best tiered
    cr1=chi1/(d['n']-2); crT=chiT/(d['n']-2*NT)
    # burkert+shells from existing sweep at canonical cap 0.4
    s=sweep[(sweep.galaxy==g)&(sweep.model=='burkert')&(np.isclose(sweep.cap,0.4))]
    if len(s):
        nsh=int(s.iloc[0]['n_shells']); bicS=float(s.iloc[0]['bic'])
        crS=float(s.iloc[0]['chi2_red']) if str(s.iloc[0]['chi2_red'])!='' else np.nan
        npts_s=int(s.iloc[0]['n_pts'])
    else:
        nsh,bicS,crS,npts_s=(-1,np.nan,np.nan,-1)
    winner=min([("Burkert",bic1),("tiers",bicT),("Burk+shells",bicS)],key=lambda z:(z[1] if np.isfinite(z[1]) else 1e9))[0]
    rows.append(dict(galaxy=g,n_pts=d['n'],n_pts_sweep=npts_s,
                     burk_chi2red=round(cr1,2),burk_bic=round(bic1,1),
                     tiers_N=NT,tiers_chi2red=round(crT,2),tiers_bic=round(bicT,1),
                     shells_n=nsh,shells_chi2red=round(crS,2) if np.isfinite(crS) else None,shells_bic=round(bicS,1) if np.isfinite(bicS) else None,
                     BIC_winner=winner))
df=pd.DataFrame(rows)
pd.set_option('display.width',200)
print(df.to_string(index=False))
df.to_csv("../compare_to_burkert.csv",index=False)

# grouped bar of chi2_red (lower=better, 1=good)
fig,ax=plt.subplots(figsize=(11,5.5))
x=np.arange(len(gals)); w=0.26
ax.bar(x-w, df.burk_chi2red, w, color='#8c564b', label='single Burkert (1 sphere)')
ax.bar(x,   df.tiers_chi2red,w, color='#1f6fb4', label='concentric tiers (best N)')
ax.bar(x+w, [c if c is not None else 0 for c in df.shells_chi2red], w, color='#c1272d', label='Burkert + shells (cap 0.4)')
for i,r in df.iterrows():
    ax.text(x[i],   r.tiers_chi2red+0.1, f"N={r.tiers_N}", ha='center', fontsize=8, color='#1f6fb4')
    if r.shells_n>=0: ax.text(x[i]+w, (r.shells_chi2red or 0)+0.1, f"{r.shells_n}sh", ha='center', fontsize=8, color='#c1272d')
ax.axhline(1.0,color='0.4',ls='--',lw=1,label='χ²_red = 1 (good fit)')
ax.set_xticks(x); ax.set_xticklabels(gals); ax.set_ylabel("χ²_red (lower = better fit)")
ax.set_title("Test 5: concentric spheres vs Burkert vs Burkert+shells",fontweight='bold')
ax.legend(fontsize=9); ax.grid(axis='y',alpha=0.25)
plt.tight_layout(); plt.savefig("../compare_to_burkert.png",dpi=140,bbox_inches="tight")
print("\nsaved compare_to_burkert.png")
