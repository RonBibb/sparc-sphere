import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import tiered_spheres as ts
from scipy.optimize import least_squares

def fit_capped(d,N,restarts,rng,a_cap):
    lo,hi=ts.bounds(N,d['rmax'])
    M_dm=max((d['vo'][-1]**2-d['v2b'][-1])*d['r'][-1]/ts.G,1e5)
    sM=max(2*d['vo'][-1]*d['ev'][-1]*d['r'][-1]/ts.G,0.05*M_dm)
    def resid(th):
        comps=ts.unpack(th,N)
        vm=np.sqrt(d['v2b']+np.clip(ts.v2dm(d['r'],th,N),0,None))
        rdat=(vm-d['vo'])/d['ev']
        Mm=sum(ts.M_burk(d['r'][-1],p0,a) for p0,a in comps)
        rdat=np.append(rdat,(Mm-M_dm)/sM)
        # hard penalty for any tier core beyond a_cap
        pen=sum(max(0.0,a-a_cap)*50 for _,a in comps)
        rdat=np.append(rdat,pen)
        return np.where(np.isfinite(rdat),rdat,1e6)
    best=None
    for _ in range(restarts):
        xi=np.clip(ts.x0(rng,N,d['rmax']),lo+1e-6,hi-1e-6)
        try: rr=least_squares(resid,xi,bounds=(lo,hi),max_nfev=5000)
        except Exception: continue
        vm=np.sqrt(d['v2b']+np.clip(ts.v2dm(d['r'],rr.x,N),0,None))
        chi2=float(np.sum(((vm-d['vo'])/d['ev'])**2))
        if best is None or chi2<best[0]: best=(chi2,rr.x)
    return best

rng=np.random.default_rng(7)
g="NGC2841"; d=ts.load(g)
# uncapped best (allow a beyond data)
unc=ts.best_tiers(d,4,20,rng)[0]; chiU,NU,thU=unc[1],unc[2],unc[3]
# capped: every tier a<=rmax, pick best N by BIC
cands=[]
for N in range(1,5):
    if d['n']-2*N<1: break
    r=fit_capped(d,N,20,rng,d['rmax'])
    if r: cands.append((r[0]+2*N*np.log(d['n']),r[0],N,r[1]))
cands.sort(); _,chiC,NC,thC=cands[0]

def oresid(th,N):
    vm=np.sqrt(d['v2b']+np.clip(ts.v2dm(d['r'],th,N),0,None))
    res=(d['vo']-vm)/d['ev']; o=d['r']>0.67*d['rmax']
    return np.mean(res[o]),vm,res
mU,vmU,resU=oresid(thU,NU); mC,vmC,resC=oresid(thC,NC)
print(f"UNCAPPED: N={NU} chi2_red={chiU/(d['n']-2*NU):.2f}  outer_resid={mU:+.2f}sigma  tiers a="+",".join(f"{a:.1f}" for _,a in ts.unpack(thU,NU)))
print(f"CAPPED  : N={NC} chi2_red={chiC/(d['n']-2*NC):.2f}  outer_resid={mC:+.2f}sigma  tiers a="+",".join(f"{a:.1f}" for _,a in ts.unpack(thC,NC))+f"  (cap={d['rmax']:.0f})")

rr=np.linspace(d['r'].min(),d['rmax'],400)
def curve(th,N):
    v2b=np.interp(rr,d['r'],d['v2b']); return np.sqrt(np.maximum(v2b+ts.v2dm(rr,th,N),0))
fig,ax=plt.subplots(2,1,figsize=(10,8),sharex=True,gridspec_kw={"height_ratios":[3,1]})
ax[0].errorbar(d['r'],d['vo'],yerr=d['ev'],fmt='o',ms=4,color='k',ecolor='0.6',capsize=2,zorder=6,label='V_obs')
ax[0].plot(rr,np.sqrt(np.maximum(np.interp(rr,d['r'],d['v2b']),0)),':',color='0.5',lw=1.5,label='baryons')
ax[0].plot(rr,curve(thU,NU),'-',color='#1f6fb4',lw=2.4,label=f'unconstrained ({NU} tiers, a_outer={ts.unpack(thU,NU)[-1][1]:.0f} kpc > r_last)')
ax[0].plot(rr,curve(thC,NC),'-',color='#c1272d',lw=2.4,label=f'tiers capped at r_last ({NC} tiers, a≤{d["rmax"]:.0f})')
ax[0].axvline(0.67*d['rmax'],color='0.7',ls='--',lw=1)
ax[0].set_ylabel("V (km/s)"); ax[0].set_title(f"{g}: can concentric spheres solve the outer rise?",fontweight='bold')
ax[0].legend(fontsize=9,loc='lower center'); ax[0].grid(alpha=0.25)
ax[1].axhline(0,color='0.5',lw=1)
ax[1].plot(d['r'],resU,'o-',ms=3,color='#1f6fb4',lw=1,label='unconstrained resid')
ax[1].plot(d['r'],resC,'s-',ms=3,color='#c1272d',lw=1,label='capped resid')
ax[1].set_xlabel("radius (kpc)"); ax[1].set_ylabel("(obs−mod)/σ"); ax[1].legend(fontsize=8); ax[1].grid(alpha=0.25)
plt.tight_layout(); plt.savefig("../ngc2841_sphere_outer_test.png",dpi=140,bbox_inches="tight")
print("saved ngc2841_sphere_outer_test.png")
