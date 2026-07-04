import os, numpy as np, pandas as pd, time, warnings
import multiprocessing as mp
warnings.filterwarnings("ignore")
import tiered_spheres as ts

CAT="../data/raw/sparc_sample123.csv"
NMAX=4; RESTARTS=20

def process(args):
    name,T=args
    warnings.filterwarnings("ignore")
    p=f"{ts.DATA}/{name}_rotmod.dat"
    if not os.path.exists(p): return None
    try: d=ts.load(name)
    except Exception: return None
    if d['n']<6: return None
    rng=np.random.default_rng(7)
    cands=ts.best_tiers(d,NMAX,RESTARTS,rng)
    if not cands: return None
    byN={c[2]:c for c in cands}
    bicB,chiB,NB,thB=cands[0]
    bic1,chi1,_,_=byN.get(1,(np.nan,np.nan,1,None))
    comps=ts.unpack(thB,NB)
    amax=max(a for _,a in comps)
    return dict(galaxy=name,T=T,n_pts=d['n'],rmax=round(d['rmax'],2),
                N_best=NB,chi2red_best=round(chiB/(d['n']-2*NB),3),bic_best=round(bicB,2),
                chi2red_burk=round(chi1/(d['n']-2),3) if np.isfinite(chi1) else None,
                bic_burk=round(bic1,2) if np.isfinite(bic1) else None,
                dBIC=round((bic1-bicB),2) if np.isfinite(bic1) else None,
                a_max=round(amax,2), a_max_gt_rmax=bool(amax>d['rmax']),
                tier_a=";".join(f"{a:.2f}" for _,a in comps))

def main():
    cat=pd.read_csv(CAT)
    gcol=next((c for c in cat.columns if c.lower() in ('galaxy','name','id')),cat.columns[0])
    tcol=next((c for c in cat.columns if c.lower() in ('t','type','ttype')),None)
    tasks=[(str(r[gcol]), (int(r[tcol]) if tcol and not pd.isna(r[tcol]) else '')) for _,r in cat.iterrows()]
    print(f"galaxies: {len(tasks)} | Nmax={NMAX} restarts={RESTARTS}",flush=True)
    t0=time.time(); rows=[]; done=0
    with mp.Pool(18) as pool:
        for r in pool.imap_unordered(process,tasks,chunksize=1):
            done+=1
            if r: rows.append(r)
            if done%15==0 or done==len(tasks):
                print(f"  ...{done}/{len(tasks)}  {time.time()-t0:.0f}s",flush=True)
    df=pd.DataFrame(rows).sort_values('galaxy')
    df.to_csv("../data/processed/tiered_spheres_full.csv",index=False)
    print(f"\ndone {len(df)} galaxies in {time.time()-t0:.0f}s -> data/processed/tiered_spheres_full.csv")
    print("\nN_best distribution:"); print(df.N_best.value_counts().sort_index().to_string())
    print(f"\nsingle Burkert sufficient (N_best=1): {(df.N_best==1).sum()} ({100*(df.N_best==1).mean():.0f}%)")
    print(f"want tiers (N_best>=2):              {(df.N_best>=2).sum()} ({100*(df.N_best>=2).mean():.0f}%)")
    imp=df[df.dBIC.notna()]
    print(f"\ntiers improve over single Burkert (dBIC>10): {(imp.dBIC>10).sum()} ({100*(imp.dBIC>10).mean():.0f}%)")
    print(f"  median dBIC (all): {imp.dBIC.median():+.1f}  | median dBIC where N>=2: {imp[imp.N_best>=2].dBIC.median():+.1f}")
    print(f"\nfit quality: median chi2red single Burkert={df.chi2red_burk.median():.2f}  vs tiers={df.chi2red_best.median():.2f}")
    print(f"galaxies still poor under tiers (chi2red>2): {(df.chi2red_best>2).sum()} ({100*(df.chi2red_best>2).mean():.0f}%)  <- likely localized-structure / shell galaxies")
    print(f"\noutermost tier extends beyond data (a_max>rmax): {df.a_max_gt_rmax.sum()} ({100*df.a_max_gt_rmax.mean():.0f}%)  <- under-constrained extended component")

if __name__=="__main__":
    mp.set_start_method("spawn",force=True)
    main()
