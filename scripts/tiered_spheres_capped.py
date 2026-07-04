import os, numpy as np, pandas as pd, time, warnings
import multiprocessing as mp
from scipy.optimize import least_squares
warnings.filterwarnings("ignore")
import tiered_spheres as ts   # reuse load, v2_burk, G

CAT="../data/raw/sparc_sample123.csv"; NMAX=4; RESTARTS=24

def unpack(theta,N,rmin,rmax):
    # theta=[p0_1, a_1, ddens_2,frac_2, ...]; a_i strictly increasing, all in [rmin,rmax]
    p0=theta[0]; a=theta[1]; comps=[(p0,a)]
    for i in range(1,N):
        p0=p0-theta[2*i]
        a=a+(rmax-a)*theta[2*i+1]   # in (a, rmax)
        comps.append((p0,a))
    return comps

def v2dm(r,theta,N,rmin,rmax):
    v=np.zeros_like(np.asarray(r,dtype=float))
    for p0,a in unpack(theta,N,rmin,rmax): v=v+ts.v2_burk(r,p0,a)
    return v

def bounds(N,rmin,rmax):
    lo=[3.0,rmin]; hi=[10.0,rmax]
    for _ in range(N-1): lo+=[0.05,0.05]; hi+=[5.0,0.95]
    return np.array(lo),np.array(hi)

def x0(rng,N,rmin,rmax):
    x=[rng.uniform(6,9), rng.uniform(rmin,max(rmin*1.01,0.3*rmax))]
    for _ in range(N-1): x+=[rng.uniform(0.3,1.5),rng.uniform(0.2,0.7)]
    return np.array(x)

def fit_N(d,N,restarts,rng):
    rmin,rmax=d['r'].min(),d['rmax']
    lo,hi=bounds(N,rmin,rmax)
    def resid(th):
        vm=np.sqrt(d['v2b']+np.clip(v2dm(d['r'],th,N,rmin,rmax),0,None))
        out=(vm-d['vo'])/d['ev']
        return np.where(np.isfinite(out),out,1e6)
    best=None
    for _ in range(restarts):
        xi=np.clip(x0(rng,N,rmin,rmax),lo+1e-9,hi-1e-9)
        try: rr=least_squares(resid,xi,bounds=(lo,hi),max_nfev=5000)
        except Exception: continue
        c=float(np.sum(rr.fun**2))
        if best is None or c<best[0]: best=(c,rr.x)
    return best

def best_tiers(d,rng):
    cand=[]
    for N in range(1,NMAX+1):
        if d['n']-2*N<1: break
        r=fit_N(d,N,RESTARTS,rng)
        if r is None: continue
        c,th=r; cand.append((c+2*N*np.log(d['n']),c,N,th))
    cand.sort(key=lambda z:z[0]); return cand

def process(args):
    name,=args; warnings.filterwarnings("ignore")
    p=f"{ts.DATA}/{name}_rotmod.dat"
    if not os.path.exists(p): return None
    try: d=ts.load(name)
    except Exception: return None
    if d['n']<6: return None
    rng=np.random.default_rng(7); c=best_tiers(d,rng)
    if not c: return None
    byN={x[2]:x for x in c}; bicB,chiB,NB,thB=c[0]
    comps=unpack(thB,NB,d['r'].min(),d['rmax'])
    return dict(galaxy=name,n_pts=d['n'],rmax=round(d['rmax'],2),N_capped=NB,
                chi2red_capped=round(chiB/(d['n']-2*NB),3),
                tier_a=";".join(f"{a:.2f}" for _,a in comps))

def main():
    cat=pd.read_csv(CAT); names=[(g,) for g in cat['Galaxy']]
    t0=time.time()
    with mp.Pool(18) as pool:
        rows=[r for r in pool.imap_unordered(process,names) if r]
    cap=pd.DataFrame(rows)
    cap.to_csv("../data/processed/tiered_spheres_capped.csv",index=False)
    print(f"done {len(cap)} galaxies in {time.time()-t0:.0f}s")
    # compare to unconstrained
    unc=pd.read_csv("../data/processed/tiered_spheres_full.csv")[['galaxy','N_best','chi2red_best']]
    m=cap.merge(unc,on='galaxy')
    print("\n--- N distribution: UNCONSTRAINED vs TWO-SIDED CAPPED ---")
    for lab,col in [("unconstrained","N_best"),("capped (a in [rmin,rmax])","N_capped")]:
        vc=m[col].value_counts().sort_index()
        print(f"  {lab:28s}: "+"  ".join(f"{int(k)}sph={int(v)}({100*v/len(m):.0f}%)" for k,v in vc.items()))
    drop=m[(m.N_best>=2)&(m.N_capped==1)]
    keep=m[(m.N_best>=2)&(m.N_capped>=2)]
    gain=m[(m.N_best==1)&(m.N_capped>=2)]
    print(f"\n  multi-sphere UNDER unconstrained: {(m.N_best>=2).sum()}")
    print(f"  of those, COLLAPSE to 1 when capped: {len(drop)} ({100*len(drop)/(m.N_best>=2).sum():.0f}%)")
    print(f"  of those, SURVIVE as >=2 when capped: {len(keep)} ({100*len(keep)/(m.N_best>=2).sum():.0f}%)")
    print(f"  multi-sphere only under capping (new): {len(gain)}")
    print(f"\n  => REAL two-sphere structure (survives two-sided cap): {(m.N_capped>=2).sum()} / {len(m)} = {100*(m.N_capped>=2).mean():.0f}%")
    print(f"     (was {100*(m.N_best>=2).mean():.0f}% unconstrained)")
    print("\n  survivors (capped N>=2):", ", ".join(sorted(m[m.N_capped>=2].galaxy)))
if __name__=="__main__":
    mp.set_start_method("spawn",force=True); main()
