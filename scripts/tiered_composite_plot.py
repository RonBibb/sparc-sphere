import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import tiered_spheres as ts

# refit the 5 galaxies (full radius), keep best-BIC tier solution, plot composite + components
gals=["NGC2841","NGC2403","NGC3521","NGC5055","NGC6946"]
rng=np.random.default_rng(7)
cols=["#2ca02c","#ff7f0e","#9467bd","#17becf"]
fig,ax=plt.subplots(2,3,figsize=(17,9)); ax=ax.ravel()
for k,g in enumerate(gals):
    d=ts.load(g)
    bic,chi2,N,th=ts.best_tiers(d,4,20,rng)[0]
    comps=ts.unpack(th,N)
    rr=np.linspace(d['r'].min(),d['rmax'],500)
    v2b=np.interp(rr,d['r'],d['v2b'])
    a=ax[k]
    a.errorbar(d['r'],d['vo'],yerr=d['ev'],fmt='o',ms=3.5,color='k',ecolor='0.6',capsize=2,zorder=6,label='V_obs')
    a.plot(rr,np.sqrt(np.maximum(v2b,0)),':',color='0.5',lw=1.5,label='baryons')
    v2tot=v2b.copy()
    for j,(p0,asc) in enumerate(comps):
        vc=ts.v2_burk(rr,p0,asc); v2tot=v2tot+vc
        a.plot(rr,np.sqrt(np.maximum(v2b+vc,0)),'--',color=cols[j],lw=1.5,
               label=f'sphere {j+1}: a={asc:.1f} kpc, logρ₀={p0:.1f}')
    a.plot(rr,np.sqrt(np.maximum(v2tot,0)),'-',color='#1f6fb4',lw=2.6,label=f'composite ({N} sphere{"s" if N>1 else ""})')
    cr=chi2/(d['n']-2*N)
    a.set_title(f"{g}  —  {N} concentric sphere{'s' if N>1 else ''},  χ²_red={cr:.2f}",fontsize=11,fontweight='bold')
    a.set_xlabel("radius (kpc)"); a.set_ylabel("V (km/s)"); a.legend(fontsize=7.5,loc='lower right'); a.grid(alpha=0.25)
ax[-1].axis('off')
fig.suptitle("Concentric decreasing-density spheres (all centered at r=0) — composite fits",fontsize=13,fontweight='bold',y=1.0)
plt.tight_layout(); plt.savefig("../tiered_composite_curves.png",dpi=140,bbox_inches="tight")
print("saved tiered_composite_curves.png")
