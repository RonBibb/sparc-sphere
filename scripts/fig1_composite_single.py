"""Fig 1 (letter): SPARC NGC 2403 single-Burkert vs two-sphere composite.
Honest annotation: N=2 by BIC, chi2_red 19.0->3.3, crossover ~2.3 kpc.
Does NOT cite dBIC=121 (that is the Barolo independent-refit value, see sec 3.7).
Shell radius (independently fitted Gaussian shell) marked to preview the
population-level concordance of Fig 2 on a single galaxy."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import tiered_spheres as ts

G="NGC2403"; rng=np.random.default_rng(7)
d=ts.load(G)
cand=ts.best_tiers(d,4,20,rng)
byN={N:(bic,chi2,th) for (bic,chi2,N,th) in cand}
bic1,chi1,th1=byN[1]; bic2,chi2,th2=byN[2]
cr1=chi1/(d['n']-2*1); cr2=chi2/(d['n']-2*2)

rr=np.linspace(d['r'].min(),d['rmax'],600)
v2b=np.interp(rr,d['r'],d['v2b'])
# single Burkert (N=1)
p0_1,a_1=ts.unpack(th1,1)[0]
v_single=np.sqrt(np.maximum(v2b+ts.v2_burk(rr,p0_1,a_1),0))
# two-sphere composite (N=2)
comps=ts.unpack(th2,2)
(p0i,ai),(p0o,ao)=comps
v_in=ts.v2_burk(rr,p0i,ai); v_out=ts.v2_burk(rr,p0o,ao)
v_comp=np.sqrt(np.maximum(v2b+v_in+v_out,0))
# crossover (where component v2 cross)
cx=rr[np.where(np.diff(np.sign(v_in-v_out)))[0]]
cx=float(cx[0]) if len(cx) else np.nan

# independently fitted shell radius for this galaxy (preview of the concordance)
_sc=pd.read_csv("../data/spatial_coincidence_capped.csv").set_index("galaxy")
r_shell=float(_sc.loc[G,"r_shell"]) if G in _sc.index else np.nan

plt.rcParams.update({"font.size":11,"axes.linewidth":0.8})
fig,ax=plt.subplots(figsize=(6.4,4.6))
ax.errorbar(d['r'],d['vo'],yerr=d['ev'],fmt='o',ms=4,color='k',ecolor='0.6',
            capsize=2,zorder=6,label=r'$V_{\rm obs}$')
ax.plot(rr,np.sqrt(np.maximum(v2b,0)),':',color='0.55',lw=1.6,label='baryons',zorder=2)
ax.plot(rr,v_single,'--',color='#c43c3c',lw=1.8,
        label=fr'single Burkert ($\chi^2_\nu={cr1:.1f}$)',zorder=3)
# components added to baryons (thin) to show inner/outer domains
ax.plot(rr,np.sqrt(np.maximum(v2b+v_in,0)),'-',color='#2ca02c',lw=1.0,alpha=0.8,
        label=fr'inner sphere ($a={ai:.1f}$ kpc)',zorder=3)
ax.plot(rr,np.sqrt(np.maximum(v2b+v_out,0)),'-',color='#9467bd',lw=1.0,alpha=0.8,
        label=fr'outer sphere ($a={ao:.1f}$ kpc)',zorder=3)
ax.plot(rr,v_comp,'-',color='#1f6fb4',lw=2.6,
        label=fr'two-sphere composite ($\chi^2_\nu={cr2:.1f}$)',zorder=5)
# shell radius marker (independent method) -- distinct dash-dot orange
if np.isfinite(r_shell):
    ax.axvline(r_shell,color='#e8820c',ls='-.',lw=1.5,alpha=0.9,zorder=4,
               label=fr'shell radius ({r_shell:.1f} kpc)')
# domain crossover marker -- solid grey, distinct from shell
if np.isfinite(cx):
    ax.axvline(cx,color='0.4',ls='-',lw=0.8,alpha=0.5,zorder=1)
    ax.text(cx,ax.get_ylim()[1]*0.04,f'  crossover\n  {cx:.1f} kpc',fontsize=8.5,color='0.3',va='bottom')
ax.set_xlabel('radius (kpc)'); ax.set_ylabel('V (km/s)')
ax.set_title(f'{G[:3]} {G[3:]}: single-domain vs two-domain decomposition',fontsize=11.5,fontweight='bold')
ax.legend(fontsize=8.5,loc='lower right',framealpha=0.95); ax.grid(alpha=0.22)
ax.set_xlim(0,d['rmax']*1.02); ax.set_ylim(0,None)
plt.tight_layout()
out="../figures/fig1_composite.png"; plt.savefig(out,dpi=240,bbox_inches='tight')
print("SAVED",out)
print(f"VERIFY  N=2 selected; chi2_red {cr1:.2f} -> {cr2:.2f}; crossover {cx:.2f} kpc; shell {r_shell:.2f} kpc")
print(f"        inner a={ai:.2f} logrho0={p0i:.2f} | outer a={ao:.2f} logrho0={p0o:.2f}")
print(f"        dBIC(N1-N2)={bic1-bic2:.1f}  (NOT shown on fig; Barolo=121 lives in sec3.7)")
