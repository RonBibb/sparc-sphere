# NESTED TEST: do shells add information AFTER spheres?
# Backbone per galaxy = FROZEN capped Burkert-sphere fit (1 or 2 spheres, BIC-selected).
# Then fit 0/1/2 shells (original erf m_shell, V^2-additive) on top. BIC-select.
# Compare to shells fit on the single-Burkert backbone (shells "before" spheres).
# Same residual space, same m_shell, same BIC as the original shell sweep.
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
from scipy.optimize import least_squares
from scipy.special import erf
import tiered_spheres as ts, tiered_spheres_capped as tc
G=4.30091e-6

def m_shell(r,M,r0,s):
    return 0.5*M*(erf((r-r0)/(s*np.sqrt(2))) - erf((-r0)/(s*np.sqrt(2))))

def fit_shells_on_backbone(d, v2dm_frozen, max_shells=2, restarts=12, cap=1.0):
    # returns list of (bic, chi2, nshell, theta, centers)
    n=d['n']; rmax=d['rmax']
    def model_extra(r, th, ns):
        v2=np.zeros_like(r)
        for i in range(ns):
            r0=th[3*i]; M=10**th[3*i+1]; s=th[3*i+2]*r0
            v2=v2+G*m_shell(r,M,r0,s)/r
        return v2
    cand=[]
    rng=np.random.default_rng(7)
    for ns in range(max_shells+1):
        if ns==0:
            chi2=float(np.sum(((d['vobs']-np.sqrt(np.clip(d['v2bar']+v2dm_frozen,0,None)))/d['ev'])**2))
            cand.append((chi2+2*np.log(n), chi2, 0, None, [])); continue
        lo=[]; hi=[]
        for _ in range(ns): lo+=[1.0,6.0,0.01]; hi+=[rmax,11.5,cap]
        lo=np.array(lo); hi=np.array(hi)
        def resid(th):
            v2=v2dm_frozen+model_extra(d['r'],th,ns)
            out=(d['vobs']-np.sqrt(np.clip(d['v2bar']+v2,0,None)))/d['ev']
            return np.where(np.isfinite(out),out,1e6)
        best=None;bx=None
        for _ in range(restarts):
            x0=[]
            for _ in range(ns): x0+=[rng.uniform(1,rmax),rng.uniform(7,10.8),rng.uniform(0.05,cap)]
            try: r=least_squares(resid,np.clip(x0,lo+1e-6,hi-1e-6),bounds=(lo,hi),method='trf',max_nfev=4000)
            except Exception: continue
            c=float(np.sum(r.fun**2))
            if best is None or c<best: best,bx=c,r.x
        if best is None: continue
        centers=[bx[3*i] for i in range(ns)]
        cand.append((best+(2+3*ns)*np.log(n), best, ns, bx, centers))
    cand.sort(key=lambda z:z[0])
    return cand

cap_tbl=pd.read_csv("../data/tiered_spheres_capped.csv").set_index('galaxy')
TS=pd.read_csv("../data/two_sphere_params.csv").set_index('galaxy')
rows=[]
for g in cap_tbl.index:
    try: d0=ts.load(g)
    except Exception: continue
    d=dict(r=d0['r'],vobs=d0['vo'],ev=d0['ev'],v2bar=d0['v2b'],n=d0['n'],rmax=d0['rmax'])
    if d['n']<8: continue
    Ncap=int(cap_tbl.loc[g,'N_capped'])
    # frozen sphere V2dm + crossover radius
    rng=np.random.default_rng(7); c=tc.best_tiers(d0,rng)
    if not c: continue
    best=c[0]; Nsel=best[2]; th=best[3]
    _comps=tc.unpack(th,Nsel,d['r'].min(),d['rmax'])
    v2sphere=np.clip(sum(ts.v2_burk(d['r'],p,a) for p,a in _comps),0,None)
    # crossover
    rx=np.nan
    if Nsel>=2:
        comps=tc.unpack(th,Nsel,d['r'].min(),d['rmax'])
        rr=np.linspace(0.05,d['rmax'],2000)
        dd=ts.v2_burk(rr,*comps[-1])-ts.v2_burk(rr,*comps[0])
        s=np.where(np.diff(np.sign(dd))!=0)[0]
        if len(s): rx=rr[s[0]]
    # shells AFTER spheres
    cand_aft=fit_shells_on_backbone(d,v2sphere)
    bic0_aft=[z[0] for z in cand_aft if z[2]==0][0]
    best_aft=cand_aft[0]
    dbic_aft=bic0_aft-best_aft[0]
    # shells BEFORE spheres (single Burkert backbone)
    p_single=None
    def rs(th):
        v2=np.clip(ts.v2_burk(d['r'],th[0],th[1]),0,None)
        return (d['vobs']-np.sqrt(d['v2bar']+v2))/d['ev']
    bb=None
    for _ in range(12):
        x0=[rng.uniform(6,9),rng.uniform(0.5,max(1,0.3*d['rmax']))]
        try: r=least_squares(rs,x0,bounds=([4,0.05],[10.5,max(2,d['rmax'])]),max_nfev=4000)
        except Exception: continue
        cc=float(np.sum(r.fun**2))
        if bb is None or cc<bb[0]: bb=(cc,r.x)
    v2single=np.clip(ts.v2_burk(d['r'],bb[1][0],bb[1][1]),0,None)
    cand_bef=fit_shells_on_backbone(d,v2single)
    best_bef=cand_bef[0]
    # crossover proximity of surviving after-shells
    near=np.nan
    if best_aft[2]>=1 and np.isfinite(rx):
        near=min(abs(np.array(best_aft[4])-rx))
    rows.append(dict(galaxy=g,Nsphere=Nsel,
        shell_before=int(best_bef[2]>0), nshell_before=best_bef[2],
        shell_after=int(best_aft[2]>0), nshell_after=best_aft[2],
        dBIC_after=round(dbic_aft,1), r_x=round(rx,2) if np.isfinite(rx) else np.nan,
        shell_center=round(best_aft[4][0],2) if best_aft[4] else np.nan,
        near_crossover_kpc=round(near,2) if np.isfinite(near) else np.nan))
R=pd.DataFrame(rows)
R.to_csv("../data/shells_after_spheres.csv",index=False)
print(f"galaxies: {len(R)}")
print(f"\nshell BEFORE spheres: {R.shell_before.sum()}/{len(R)}")
print(f"shell AFTER spheres:  {R.shell_after.sum()}/{len(R)}")
print(f"\n--- among 2-sphere galaxies (N={int((R.Nsphere>=2).sum())}) ---")
two=R[R.Nsphere>=2]
print(f"shell before: {two.shell_before.sum()}/{len(two)}  |  shell after: {two.shell_after.sum()}/{len(two)}")
print(f"shells ABSORBED by 2nd sphere (before=yes, after=no): {((two.shell_before==1)&(two.shell_after==0)).sum()}")
print(f"shells SURVIVE spheres (after=yes, strong dBIC>10): {((two.shell_after==1)&(two.dBIC_after>10)).sum()}")
surv=two[(two.shell_after==1)&(two.dBIC_after>10)]
if len(surv):
    print("\nSURVIVORS (shell distinct from broad domain):")
    print(surv[['galaxy','dBIC_after','shell_center','r_x','near_crossover_kpc']].to_string(index=False))
