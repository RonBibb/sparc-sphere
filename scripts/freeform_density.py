# Non-parametric DM density fit: solve rho in log-spaced radial bins.
# Model: V2_dm(r) = G * M(<r)/r, with M(<r)=4*pi*integral rho r^2 dr over bins.
# Free params = log10(rho_b) per bin. ONLY prior = smoothness in log-log (curvature penalty).
# No functional form, no ordering, no core/cusp imposed.
import numpy as np, warnings
from scipy.optimize import least_squares
warnings.filterwarnings("ignore")
import tiered_spheres as ts
G=ts.G

def shell_mass_matrix(r_data, edges):
    # enclosed mass at each r_data from piecewise-constant rho in bins [edges]
    # M(<r) = sum_b rho_b * Vol(bin_b up to r)
    nb=len(edges)-1
    Aenc=np.zeros((len(r_data),nb))
    for i,r in enumerate(r_data):
        for b in range(nb):
            lo,hi=edges[b],min(edges[b+1],r)
            if hi>lo:
                Aenc[i,b]=4*np.pi/3*(hi**3-lo**3)   # volume of spherical bin slice
    return Aenc

def fit_freeform(d, nbin=None, smooth=3.0):
    if nbin is None: nbin=max(5,min(12,d['n']//2))
    r=d['r']; rmin,rmax=r.min(),r.max()
    edges=np.logspace(np.log10(rmin*0.5),np.log10(rmax),nbin+1)
    A=shell_mass_matrix(r,edges)              # (npts, nbin) enclosed-volume matrix
    bc=np.sqrt(edges[:-1]*edges[1:])          # bin centers (log)
    def resid(logrho):
        rho=10**logrho
        Menc=A@rho
        v2=G*Menc/r
        vm=np.sqrt(d['v2b']+np.clip(v2,0,None))
        dat=(vm-d['vo'])/d['ev']
        # smoothness prior: penalize 2nd derivative of logrho in log-r (curvature)
        d2=np.diff(logrho,2)
        return np.concatenate([dat, smooth*d2])
    x0=np.full(nbin,7.0)
    lo=np.full(nbin,2.0); hi=np.full(nbin,11.0)
    rr=least_squares(resid,x0,bounds=(lo,hi),max_nfev=20000)
    logrho=rr.x; rho=10**logrho
    # data fit only (exclude prior) for chi2
    Menc=A@rho; v2=G*Menc/r; vm=np.sqrt(d['v2b']+np.clip(v2,0,None))
    chi2=float(np.sum(((vm-d['vo'])/d['ev'])**2))
    # inner log-log slope: gamma = -dln rho/dln r over inner ~3 bins
    inner=slice(0,4)
    sl=np.polyfit(np.log(bc[inner]),np.log(np.maximum(rho[inner],1)),1)[0]
    gamma=-sl
    return dict(bc=bc,rho=rho,chi2=chi2,chi2red=chi2/max(1,len(r)-nbin),inner_slope=gamma,edges=edges)

if __name__=="__main__":
    import pandas as pd, matplotlib
    matplotlib.use("Agg"); import matplotlib.pyplot as plt
    gals=["NGC2403","NGC2841","NGC3521","NGC5055","DDO154","NGC6503"]
    fig,ax=plt.subplots(2,3,figsize=(15,9))
    for a,g in zip(ax.flat,gals):
        d=ts.load(g); f=fit_freeform(d)
        a.loglog(f['bc'],f['rho'],'o-',color='#1f6fb4',lw=1.8,ms=4,label='free-form ρ(r)')
        # reference slopes
        rr=np.array([f['bc'][0],f['bc'][3]])
        a.loglog(rr, f['rho'][0]*(rr/rr[0])**0,'--',color='gray',alpha=0.6,label='core (γ=0)')
        a.loglog(rr, f['rho'][0]*(rr/rr[0])**-1,':',color='red',alpha=0.7,label='cusp (γ=1, NFW)')
        a.set_title(f"{g}: inner slope γ={f['inner_slope']:.2f}  (χ²r={f['chi2red']:.1f})",fontsize=10,fontweight='bold')
        a.set_xlabel("r (kpc)"); a.set_ylabel("ρ_DM (M⊙/kpc³)"); a.legend(fontsize=7); a.grid(alpha=0.25,which='both')
    plt.tight_layout(); plt.savefig("../freeform_density.png",dpi=140,bbox_inches="tight")
    print("inner-slope summary (γ=0 core, γ=1 NFW cusp):")
    for g in gals:
        d=ts.load(g); f=fit_freeform(d)
        print(f"  {g:10s} γ_inner={f['inner_slope']:+.2f}  χ²red={f['chi2red']:.2f}")
    print("saved freeform_density.png")
