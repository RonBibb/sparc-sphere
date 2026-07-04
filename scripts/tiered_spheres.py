"""
tiered_spheres.py -- constrained concentric-sphere halo decomposition.

N cored (Burkert) spheres with, OUTWARD:
   rho0 strictly DECREASING  and  core radius a strictly INCREASING
enforced by ratio parameterization (cannot collapse to same scale).
Soft DM mass-closure to the outermost included point, weighted by its error.
BIC-select N (k = 2N). Fit full-radius and inner-2/3.

Tests: (1) do the constraints break the same-scale degeneracy seen in burkert3?
       (2) does the sphere stack leave an outer-tail RISE unfit? (prediction: yes)
"""
import os, numpy as np, pandas as pd, warnings
from scipy.optimize import least_squares
warnings.filterwarnings("ignore")

G=4.30091e-6; YD,YB=0.5,0.7; SIG=1.0
DATA="/Users/ronbibb/Library/CloudStorage/OneDrive-Personal(2)/Documents/Academic/Rotmod_LTG"

def v2_burk(r,p0,a):
    rho0=10**p0; a=max(a,1e-6)
    M=np.pi*rho0*a**3*(np.log(1+r**2/a**2)+2*np.log(1+r/a)-2*np.arctan(r/a))
    return np.maximum(G*M/np.maximum(r,1e-6),0)
def M_burk(r,p0,a):
    rho0=10**p0; a=max(a,1e-6)
    return np.pi*rho0*a**3*(np.log(1+r**2/a**2)+2*np.log(1+r/a)-2*np.arctan(r/a))

def load(g):
    d=np.loadtxt(f"{DATA}/{g}_rotmod.dat",comments="#")
    r,vo,ev,vg,vd,vb=d[:,0],d[:,1],d[:,2],d[:,3],d[:,4],d[:,5]
    v2b=vg*np.abs(vg)+YD*vd*np.abs(vd)+YB*vb*np.abs(vb)
    ev=np.maximum(ev,SIG); keep=v2b<vo*np.abs(vo)
    return dict(r=r[keep],vo=vo[keep],ev=ev[keep],v2b=v2b[keep],
                rmax=float(r[keep].max()),n=int(keep.sum()))

def unpack(theta,N):
    """theta=[p0_1, a_1, ddens_2,dcore_2, ddens_3,dcore_3, ...] -> [(p0_i,a_i)] monotone."""
    comps=[(theta[0], theta[1])]; p0=theta[0]; a=theta[1]
    for i in range(1,N):
        p0=p0 - theta[2*i]          # density drops (ddens>0)
        a =a * 10**theta[2*i+1]     # core grows  (dcore>0)
        comps.append((p0,a))
    return comps

def v2dm(r,theta,N):
    v=np.zeros_like(np.asarray(r,dtype=float))
    for p0,a in unpack(theta,N): v=v+v2_burk(r,p0,a)
    return v

def bounds(N,rmax):
    lo=[3.0,0.10]; hi=[10.0,rmax*1.5]          # p0_1, a_1 (ceiling raised to 1e10)
    for _ in range(N-1):
        lo+=[0.05,0.05]; hi+=[5.0,1.5]         # min density-drop & min core-growth -> strict order
    return np.array(lo),np.array(hi)

def x0(rng,N,rmax):
    x=[rng.uniform(6,9), rng.uniform(0.5,max(1.0,0.2*rmax))]
    for _ in range(N-1): x+=[rng.uniform(0.3,1.5), rng.uniform(0.2,0.8)]
    return np.array(x)

def fit_N(d,N,restarts,rng,mass_closure=True):
    lo,hi=bounds(N,d['rmax'])
    # DM mass at outer included point + its error
    M_dm = max((d['vo'][-1]**2 - d['v2b'][-1])*d['r'][-1]/G, 1e5)
    sM   = max(2*d['vo'][-1]*d['ev'][-1]*d['r'][-1]/G, 0.05*M_dm)
    def resid(th):
        vm=np.sqrt(d['v2b']+np.clip(v2dm(d['r'],th,N),0,None))
        rdat=(vm-d['vo'])/d['ev']
        if mass_closure:
            Mm=sum(M_burk(d['r'][-1],p0,a) for p0,a in unpack(th,N))
            rdat=np.append(rdat,(Mm-M_dm)/sM)
        return np.where(np.isfinite(rdat),rdat,1e6)
    best=None
    for _ in range(restarts):
        xi=np.clip(x0(rng,N,d['rmax']),lo+1e-6,hi-1e-6)
        try: rr=least_squares(resid,xi,bounds=(lo,hi),method='trf',max_nfev=5000)
        except Exception: continue
        # chi2 over DATA points only (exclude closure prior)
        vm=np.sqrt(d['v2b']+np.clip(v2dm(d['r'],rr.x,N),0,None))
        chi2=float(np.sum(((vm-d['vo'])/d['ev'])**2))
        if best is None or chi2<best[0]: best=(chi2,rr.x)
    return best

def best_tiers(d,Nmax,restarts,rng):
    cand=[]
    for N in range(1,Nmax+1):
        if d['n']-2*N<1: break
        r=fit_N(d,N,restarts,rng)
        if r is None: continue
        chi2,th=r; bic=chi2+2*N*np.log(d['n'])
        cand.append((bic,chi2,N,th))
    cand.sort(key=lambda z:z[0])
    return cand

def outer_resid(d,th,N):
    vm=np.sqrt(d['v2b']+np.clip(v2dm(d['r'],th,N),0,None))
    res=(d['vo']-vm)/d['ev']
    outer=d['r']>0.67*d['rmax']
    return float(np.mean(res[outer])), int(outer.sum())

if __name__=="__main__":
    gals=["NGC2841","NGC2403","NGC3521","NGC5055","NGC6946"]
    rng=np.random.default_rng(7)
    print(f"{'galaxy':10s} {'n':>3s} {'rmax':>5s} | full: N chi2_red  | inner2/3: N chi2_red | outer_resid(full)")
    rows=[]
    for g in gals:
        d=load(g)
        full=best_tiers(d,4,16,rng)[0]
        # inner 2/3
        cut=d['r']<=0.67*d['rmax']
        di=dict(r=d['r'][cut],vo=d['vo'][cut],ev=d['ev'][cut],v2b=d['v2b'][cut],
                rmax=float(d['r'][cut].max()),n=int(cut.sum()))
        inner=best_tiers(di,4,16,rng)[0]
        bicF,chiF,NF,thF=full; bicI,chiI,NI,thI=inner
        crF=chiF/(d['n']-2*NF); crI=chiI/(di['n']-2*NI)
        mres,nout=outer_resid(d,thF,NF)
        # report the monotone params to verify no collapse
        cF=unpack(thF,NF)
        ascale="; ".join(f"a{j+1}={a:.2f}" for j,(p0,a) in enumerate(cF))
        print(f"{g:10s} {d['n']:3d} {d['rmax']:5.1f} | full: {NF} {crF:7.2f}  | inner:    {NI} {crI:7.2f} | mean_outer_resid={mres:+.2f}sigma ({nout}pts)")
        print(f"           tiers(full): {ascale}")
        rows.append(dict(galaxy=g,n=d['n'],rmax=round(d['rmax'],1),N_full=NF,chi2red_full=round(crF,2),
                         N_inner=NI,chi2red_inner=round(crI,2),outer_resid_sigma=round(mres,2),n_outer=nout))
    pd.DataFrame(rows).to_csv("../data/processed/tiered_spheres_validation.csv",index=False)
    print("\nsaved data/processed/tiered_spheres_validation.csv")
