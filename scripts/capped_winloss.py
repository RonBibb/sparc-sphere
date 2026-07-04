import os, numpy as np, pandas as pd, warnings, multiprocessing as mp
warnings.filterwarnings("ignore")
import tiered_spheres as ts, tiered_spheres_capped as tc
def proc(args):
    name,=args; warnings.filterwarnings("ignore")
    if not os.path.exists(f"{ts.DATA}/{name}_rotmod.dat"): return None
    try: d=ts.load(name)
    except Exception: return None
    if d['n']<6: return None
    rng=np.random.default_rng(7); c=tc.best_tiers(d,rng); byN={x[2]:x for x in c}
    if 1 not in byN or 2 not in byN: return None
    b1,c1=byN[1][0],byN[1][1]; b2,c2=byN[2][0],byN[2][1]
    return dict(galaxy=name,n=d['n'],N_best=c[0][2],bic1=b1,bic2=b2,
                margin=b2-b1, chi2gain=c1-c2)
def main():
    cat=pd.read_csv("../data/raw/sparc_sample123.csv")
    with mp.Pool(18) as pool:
        rows=[r for r in pool.imap_unordered(proc,[(g,) for g in cat['Galaxy']]) if r]
    m=pd.DataFrame(rows).merge(cat,left_on='galaxy',right_on='Galaxy',how='left')
    win=m[m.margin<0]   # 2 spheres beat 1
    lose=m[m.margin>=0]
    print(f"CAPPED concentric-sphere win/loss vs single Burkert:")
    print(f"  2 spheres WIN:  {len(win)}  ({100*len(win)/len(m):.0f}%)")
    print(f"  single Burkert WIN (2 lose): {len(lose)}  ({100*len(lose)/len(m):.0f}%)")
    print(f"\n--- when 2 spheres WIN, by how much (BIC_1 - BIC_2) ---")
    wm=-win.margin
    print(f"  median +{wm.median():.1f}  | strong(>10): {(wm>10).sum()}  decisive(>30): {(wm>30).sum()}  max +{wm.max():.0f}")
    print(f"--- when 2 spheres LOSE, by how much (BIC_2 - BIC_1) ---")
    lm=lose.margin
    print(f"  median +{lm.median():.1f}  | near-miss(<6): {(lm<6).sum()} ({100*(lm<6).mean():.0f}%)  decisive Burkert(>10): {(lm>=10).sum()}")
    print(f"\nmass split: 2-sphere winners medVflat={win.Vflat.median():.0f}  vs single medVflat={lose.Vflat.median():.0f}")
    m.to_csv("../capped_winloss.csv",index=False)
if __name__=="__main__":
    mp.set_start_method("spawn",force=True); main()
