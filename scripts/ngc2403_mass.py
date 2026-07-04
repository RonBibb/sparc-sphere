import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import tiered_spheres as ts

g="NGC2403"; d=ts.load(g)
r,vo,ev,v2b=d['r'],d['vo'],d['ev'],d['v2b']
G=ts.G
# enclosed masses
M_dyn = vo**2*r/G
sM    = 2*vo*ev*r/G
M_bar = np.maximum(v2b,0)*r/G
v2dm_data = np.maximum(vo**2-v2b,0)
M_dm  = v2dm_data*r/G
sM_dm = 2*vo*ev*r/G

# smooth concentric-sphere model
rng=np.random.default_rng(7)
bic,chi2,N,th=ts.best_tiers(d,4,20,rng)[0]
rr=np.linspace(r.min(),r.max(),600)
M_dm_model = np.array([sum(ts.M_burk(x,p0,a) for p0,a in ts.unpack(th,N)) for x in rr])
comps=ts.unpack(th,N)

fig,ax=plt.subplots(2,1,figsize=(10,9),sharex=True,gridspec_kw={"height_ratios":[3,2]})
# --- cumulative mass ---
a0=ax[0]
a0.errorbar(r,M_dyn,yerr=sM,fmt='o',ms=4,color='k',ecolor='0.6',capsize=2,label='total dynamical M(<r)')
a0.plot(r,M_bar,'s-',ms=3,color='#8c564b',lw=1,alpha=0.7,label='baryonic M(<r)')
a0.errorbar(r,M_dm,yerr=sM_dm,fmt='^',ms=4,color='#1f6fb4',ecolor='#9ec9e8',capsize=2,label='dark-matter M(<r) [data]')
a0.plot(rr,M_dm_model,'-',color='#c1272d',lw=2.2,label=f'DM smooth model ({N} concentric spheres)')
for j,(p0,asc) in enumerate(comps):
    Mc=np.array([ts.M_burk(x,p0,asc) for x in rr])
    a0.plot(rr,Mc,'--',color=['#2ca02c','#ff7f0e','#9467bd'][j],lw=1.2,alpha=0.8,label=f'sphere {j+1} (a={asc:.1f})')
a0.set_yscale('log'); a0.set_ylabel(r"M(<r)  [M$_\odot$]"); a0.grid(alpha=0.25,which='both')
a0.set_title(f"{g} — enclosed mass",fontweight='bold'); a0.legend(fontsize=8,loc='lower right')
# --- local mass accumulation rate dM/dr (DM) ---
a1=ax[1]
dMdr_data = np.gradient(M_dm, r)
dMdr_model= np.gradient(M_dm_model, rr)
a1.plot(r,dMdr_data,'o-',ms=4,color='#1f6fb4',lw=1.2,label='dM/dr  DM [data]')
a1.plot(rr,dMdr_model,'-',color='#c1272d',lw=2.0,label='dM/dr  DM smooth model')
a1.axhline(0,color='0.6',lw=0.8)
# shade high-error region 3-5 kpc
a1.axvspan(2.9,5.0,color='orange',alpha=0.12,label='high-errV band (2.9-5 kpc)')
a1.set_xlabel("radius (kpc)"); a1.set_ylabel(r"dM/dr  [M$_\odot$/kpc]"); a1.grid(alpha=0.25)
a1.legend(fontsize=8,loc='upper right')
plt.tight_layout(); plt.savefig("../ngc2403_mass.png",dpi=140,bbox_inches="tight")
print(f"{g}: N={N} spheres, tiers a="+", ".join(f"{a:.2f}" for _,a in comps))
print(f"  M_dyn(<rmax)={M_dyn[-1]:.3e}  M_bar={M_bar[-1]:.3e}  M_dm={M_dm[-1]:.3e}  (DM/bar={M_dm[-1]/M_bar[-1]:.1f})")
print("saved ngc2403_mass.png")
