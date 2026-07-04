import os, numpy as np, pandas as pd, time, warnings
import multiprocessing as mp
warnings.filterwarnings("ignore")
import tiered_spheres as ts

CAT="../data/raw/sparc_sample123.csv"
def proc(args):
    name,=args
    warnings.filterwarnings("ignore")
    p=f"{ts.DATA}/{name}_rotmod.dat"
    if not os.path.exists(p): return None
    try: d=ts.load(name)
    except Exception: return None
    if d['n']<6: return None
    rng=np.random.default_rng(7)
    cands=ts.best_tiers(d,4,20,rng); byN={c[2]:c for c in cands}
    if 1 not in byN or 2 not in byN: return None
    b1,c1,_,_=byN[1]; b2,c2,_,_=byN[2]
    NB=cands[0][2]
    return dict(galaxy=name,n=d['n'],N_best=NB,
        chi2_1=c1,bic_1=b1,chi2_2=c2,bic_2=b2,
        bic_margin=b2-b1,            # >0 => 2 spheres LOSE
        chi2_gain=c1-c2)            # how much chi2 improved with 2nd sphere
def main():
    cat=pd.read_csv(CAT); names=[(g,) for g in cat['Galaxy']]
    with mp.Pool(18) as pool:
        rows=[r for r in pool.imap_unordered(proc,names) if r]
    m=pd.DataFrame(rows).merge(cat,left_on='galaxy',right_on='Galaxy',how='left')
    m.to_csv("../two_vs_one_margins.csv",index=False)
    lose=m[m.N_best==1]   # single Burkert won => 2 spheres lost
    win =m[m.N_best>=2]
    print(f"single-Burkert wins (2 spheres lose): {len(lose)}   |   2+ spheres win: {len(win)}")
    print("\n--- among the {} where 2 spheres LOSE, by how much (BIC_2 - BIC_1) ---".format(len(lose)))
    bm=lose.bic_margin
    print(f"  median margin = {bm.median():.1f}  (positive = Burkert better)")
    print(f"  NEAR-MISS (lost by <6, 2nd sphere nearly justified): {(bm<6).sum()} ({100*(bm<6).mean():.0f}%)")
    print(f"  moderate   (6-10):                                   {((bm>=6)&(bm<10)).sum()}")
    print(f"  DECISIVE   (Burkert wins by >10):                    {(bm>=10).sum()} ({100*(bm>=10).mean():.0f}%)")
    print(f"\n  did the 2nd sphere improve chi2 at all? (chi2 gain>2): {(lose.chi2_gain>2).sum()}/{len(lose)}")
    print(f"    -> these {(lose.chi2_gain>2).sum()} fit a bit better but the BIC penalty killed the 2nd sphere")
    print(f"  2nd sphere essentially useless (chi2 gain<2):          {(lose.chi2_gain<2).sum()}/{len(lose)}")
    # characteristics
    print(f"\n--- who are the single-Burkert (2-spheres-lose) galaxies? ---")
    for col,lab in [('Vflat','V_flat'),('logM_star','logM*')]:
        print(f"  {lab}: lose median={lose[col].median():.1f}  vs  win median={win[col].median():.1f}")
    print(f"  dwarfs (Vflat<80) among losers: {(lose.Vflat<80).sum()}/{len(lose)} ({100*(lose.Vflat<80).mean():.0f}%)")
    # the near-miss galaxies (interesting middle ground)
    nm=lose[lose.bic_margin<6].sort_values('bic_margin')
    print(f"\n  NEAR-MISS galaxies (2nd sphere almost won, sorted by margin):")
    print("   "+", ".join(f"{g}({mr:.1f})" for g,mr in zip(nm.galaxy.head(15),nm.bic_margin.head(15))))
if __name__=="__main__":
    mp.set_start_method("spawn",force=True); main()
