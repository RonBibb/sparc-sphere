# FREE-ALPHA EINASTO null test (referee response).
# Q: the fixed-shape (alpha=0.16) Einasto null inflates the two-domain fraction to 54%
#    vs 35-37% for Burkert/NFW. Is that because fixed-shape Einasto is too rigid to absorb
#    inner structure with ONE component? Test: free alpha -> does the fraction drop to ~35%?
# Design: alpha is a SINGLE extra global shape parameter for the galaxy (shared by all domains).
#    So N-domain free-alpha Einasto has k = 2N + 1 params. BIC penalty counts the +1 fairly.
import os, numpy as np, pandas as pd, time, warnings, multiprocessing as mp
from scipy.optimize import least_squares
from scipy.special import gammainc, gamma as gammafn
warnings.filterwarnings("ignore")
import tiered_spheres as ts
G=ts.G

def M_eina_a(r,p0,a,alpha):
    rho=10**p0; a=max(a,1e-6); alpha=min(max(alpha,0.03),0.8); s=np.maximum(r,1e-9)/a
    c=4*np.pi*rho*a**3*(1.0/alpha)*np.exp(2.0/alpha)*(2.0/alpha)**(-3.0/alpha)*gammafn(3.0/alpha)
    return c*gammainc(3.0/alpha,(2.0/alpha)*s**alpha)

def unpack(theta,N):
    # theta = [p0_0,a_0, dp_1,la_1, ..., alpha]  (alpha is LAST, shared)
    alpha=theta[-1]
    comps=[(theta[0],theta[1])]; p0=theta[0]; a=theta[1]
    for i in range(1,N):
        p0=p0-theta[2*i]; a=a*10**theta[2*i+1]; comps.append((p0,a))
    return comps,alpha
def v2dm(r,theta,N):
    comps,alpha=unpack(theta,N); v=np.zeros_like(np.asarray(r,float))
    for p0,a in comps: v=v+np.maximum(G*M_eina_a(r,p0,a,alpha)/np.maximum(r,1e-6),0)
    return v
def bounds(N,rmax):
    lo=[3.0,0.10]; hi=[10.0,rmax*1.5]
    for _ in range(N-1): lo+=[0.05,0.05]; hi+=[5.0,1.5]
    lo+=[0.10]; hi+=[0.30]    # alpha bounds (physical Einasto shape range)
    return np.array(lo),np.array(hi)
def x0(rng,N,rmax):
    x=[rng.uniform(6,9),rng.uniform(0.5,max(1.0,0.2*rmax))]
    for _ in range(N-1): x+=[rng.uniform(0.3,1.5),rng.uniform(0.2,0.8)]
    x+=[rng.uniform(0.12,0.25)]  # alpha start near canonical
    return np.array(x)
def fit_N(d,N,restarts,rng):
    lo,hi=bounds(N,d['rmax'])
    M_dm=max((d['vo'][-1]**2-d['v2b'][-1])*d['r'][-1]/G,1e5)
    sM=max(2*d['vo'][-1]*d['ev'][-1]*d['r'][-1]/G,0.05*M_dm)
    def resid(th):
        vm=np.sqrt(d['v2b']+np.clip(v2dm(d['r'],th,N),0,None))
        rdat=(vm-d['vo'])/d['ev']
        comps,al=unpack(th,N)
        Mm=sum(M_eina_a(d['r'][-1],p0,a,al) for p0,a in comps)
        rdat=np.append(rdat,(Mm-M_dm)/sM)
        return np.where(np.isfinite(rdat),rdat,1e6)
    best=None
    for _ in range(restarts):
        xi=np.clip(x0(rng,N,d['rmax']),lo+1e-6,hi-1e-6)
        try: rr=least_squares(resid,xi,bounds=(lo,hi),method='trf',max_nfev=6000)
        except Exception: continue
        vm=np.sqrt(d['v2b']+np.clip(v2dm(d['r'],rr.x,N),0,None))
        c=float(np.sum(((vm-d['vo'])/d['ev'])**2))
        if best is None or c<best[0]: best=(c,rr.x)
    return best
def best_N(d,rng,Nmax=4,restarts=20):
    cand=[]
    for N in range(1,Nmax+1):
        k=2*N+1                      # +1 for shared alpha
        if d['n']-k<1: break
        r=fit_N(d,N,restarts,rng)
        if r is None: continue
        c,th=r
        cand.append((c+k*np.log(d['n']),c,N,th[-1]))
    cand.sort(); return cand[0] if cand else None
def proc(args):
    name=args; warnings.filterwarnings("ignore")
    if not os.path.exists(f"{ts.DATA}/{name}_rotmod.dat"): return None
    try: d=ts.load(name)
    except Exception: return None
    if d['n']<7: return None
    rng=np.random.default_rng(7); b=best_N(d,rng)
    if b is None: return None
    return dict(galaxy=name,N_best=b[2],alpha=round(b[3],3),chi2=round(b[1],2))
def main():
    cat=pd.read_csv("../data/raw/sparc_sample123.csv")
    t0=time.time()
    with mp.Pool(min(8,mp.cpu_count())) as pool:
        res=[r for r in pool.map(proc,list(cat['Galaxy'])) if r]
    D=pd.DataFrame(res); D.to_csv("../data/einasto_phys_alpha.csv",index=False)
    n=len(D); 
    print(f"physical-alpha (0.1-0.3) Einasto: {n} galaxies, {time.time()-t0:.0f}s\n")
    vc=D.N_best.value_counts().sort_index()
    for k,v in vc.items(): print(f"  N={k}: {v} ({100*v/n:.0f}%)")
    f2=100*(D.N_best>=2).sum()/n
    print(f"\n  TWO-DOMAIN FRACTION (free-alpha Einasto): {f2:.0f}%")
    print(f"  compare: fixed-alpha Einasto 54%, Burkert 35%, NFW 37%")
    print(f"\n  fitted alpha: median {D.alpha.median():.3f} [{D.alpha.quantile(.16):.3f}-{D.alpha.quantile(.84):.3f}]")
    print(f"  (fixed null used 0.16)")
if __name__=="__main__": main()
