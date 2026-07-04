# Minimum-order concentric-domain decomposition for THREE backbones: Burkert, NFW, Einasto.
# Each domain = 2 params (log rho, scale a); density decreasing + scale increasing outward.
# BIC-selects N (k=2N). Same machinery for all three -> fair grid. Einasto alpha fixed=0.16
# so every backbone has 2 params/domain (fair BIC).
import os, numpy as np, pandas as pd, time, warnings, multiprocessing as mp
from scipy.optimize import least_squares
from scipy.special import gammainc, gamma as gammafn
warnings.filterwarnings("ignore")
import tiered_spheres as ts
G=ts.G; ALPHA=0.16

def M_burk(r,p0,a):
    rho=10**p0; a=max(a,1e-6)
    return np.pi*rho*a**3*(np.log(1+r**2/a**2)+2*np.log(1+r/a)-2*np.arctan(r/a))
def M_nfw(r,p0,a):
    rho=10**p0; a=max(a,1e-6); x=np.maximum(r,1e-9)/a
    return 4*np.pi*rho*a**3*(np.log(1+x)-x/(1+x))
def M_eina(r,p0,a):
    rho=10**p0; a=max(a,1e-6); s=np.maximum(r,1e-9)/a
    c=4*np.pi*rho*a**3*(1.0/ALPHA)*np.exp(2.0/ALPHA)*(2.0/ALPHA)**(-3.0/ALPHA)*gammafn(3.0/ALPHA)
    return c*gammainc(3.0/ALPHA,(2.0/ALPHA)*s**ALPHA)
MFUN={'burkert':M_burk,'nfw':M_nfw,'einasto':M_eina}

def unpack(theta,N):
    comps=[(theta[0],theta[1])]; p0=theta[0]; a=theta[1]
    for i in range(1,N):
        p0=p0-theta[2*i]; a=a*10**theta[2*i+1]; comps.append((p0,a))
    return comps
def v2dm(r,theta,N,Mf):
    v=np.zeros_like(np.asarray(r,float))
    for p0,a in unpack(theta,N): v=v+np.maximum(G*Mf(r,p0,a)/np.maximum(r,1e-6),0)
    return v
def bounds(N,rmax):
    lo=[3.0,0.10]; hi=[10.0,rmax*1.5]
    for _ in range(N-1): lo+=[0.05,0.05]; hi+=[5.0,1.5]
    return np.array(lo),np.array(hi)
def x0(rng,N,rmax):
    x=[rng.uniform(6,9),rng.uniform(0.5,max(1.0,0.2*rmax))]
    for _ in range(N-1): x+=[rng.uniform(0.3,1.5),rng.uniform(0.2,0.8)]
    return np.array(x)
def fit_N(d,N,Mf,restarts,rng):
    lo,hi=bounds(N,d['rmax'])
    M_dm=max((d['vo'][-1]**2-d['v2b'][-1])*d['r'][-1]/G,1e5)
    sM=max(2*d['vo'][-1]*d['ev'][-1]*d['r'][-1]/G,0.05*M_dm)
    def resid(th):
        vm=np.sqrt(d['v2b']+np.clip(v2dm(d['r'],th,N,Mf),0,None))
        rdat=(vm-d['vo'])/d['ev']
        Mm=sum(Mf(d['r'][-1],p0,a) for p0,a in unpack(th,N))
        rdat=np.append(rdat,(Mm-M_dm)/sM)
        return np.where(np.isfinite(rdat),rdat,1e6)
    best=None
    for _ in range(restarts):
        xi=np.clip(x0(rng,N,d['rmax']),lo+1e-6,hi-1e-6)
        try: rr=least_squares(resid,xi,bounds=(lo,hi),method='trf',max_nfev=5000)
        except Exception: continue
        vm=np.sqrt(d['v2b']+np.clip(v2dm(d['r'],rr.x,N,Mf),0,None))
        c=float(np.sum(((vm-d['vo'])/d['ev'])**2))
        if best is None or c<best[0]: best=(c,rr.x)
    return best
def best_N(d,Mf,rng,Nmax=4,restarts=20):
    cand=[]
    for N in range(1,Nmax+1):
        if d['n']-2*N<1: break
        r=fit_N(d,N,Mf,restarts,rng)
        if r is None: continue
        c,th=r; cand.append((c+2*N*np.log(d['n']),c,N))
    cand.sort(); return cand[0] if cand else None

def proc(args):
    name,model=args; warnings.filterwarnings("ignore")
    if not os.path.exists(f"{ts.DATA}/{name}_rotmod.dat"): return None
    try: d=ts.load(name)
    except Exception: return None
    if d['n']<6: return None
    rng=np.random.default_rng(7); b=best_N(d,MFUN[model],rng)
    if b is None: return None
    return dict(galaxy=name,model=model,N_best=b[2],chi2red=round(b[1]/(d['n']-2*b[2]),3))

def main():
    cat=pd.read_csv("../data/raw/sparc_sample123.csv")
    tasks=[(g,m) for m in ['burkert','nfw','einasto'] for g in cat['Galaxy']]
    t0=time.time()
    with mp.Pool(18) as pool:
        rows=[r for r in pool.imap_unordered(proc,tasks) if r]
    m=pd.DataFrame(rows); m.to_csv("../tiered_multimodel.csv",index=False)
    print(f"done {len(m)} fits ({len(m)//3} galaxies x 3 models) in {time.time()-t0:.0f}s\n")
    print("=== GRID: counts by model x N_best ===")
    grid=m.pivot_table(index='model',columns='N_best',values='galaxy',aggfunc='count',fill_value=0)
    print(grid.to_string())
    print("\n=== WIN/LOSS vs single profile (N=1 win) ===")
    for mod in ['nfw','burkert','einasto']:
        s=m[m.model==mod]; n=len(s); one=(s.N_best==1).sum(); multi=(s.N_best>=2).sum()
        print(f"  {mod:8s}: 1-domain WIN {one:3d} ({100*one/n:.0f}%)  |  multi-domain {multi:3d} ({100*multi/n:.0f}%)  [N={n}]")
if __name__=="__main__":
    mp.set_start_method("spawn",force=True); main()
