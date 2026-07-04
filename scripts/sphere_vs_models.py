# WIN/LOSS: existing concentric-sphere composite (FROZEN) vs single NFW / Burkert / Einasto.
# Spheres are NOT refit. We only fit the 3 single-profile opponents, then score per galaxy,
# broken out by the sphere model's domain count. Both capped & uncapped sphere sets; BIC & chi2_red.
import os, numpy as np, pandas as pd, warnings, multiprocessing as mp
warnings.filterwarnings("ignore")
import tiered_spheres as ts, tiered_multi as tm

def fit_single(args):
    name,model=args; warnings.filterwarnings("ignore")
    if not os.path.exists(f"{ts.DATA}/{name}_rotmod.dat"): return None
    try: d=ts.load(name)
    except Exception: return None
    if d['n']<6: return None
    rng=np.random.default_rng(7)
    r=tm.fit_N(d,1,tm.MFUN[model],24,rng)   # single profile = 1 domain, k=2
    if r is None: return None
    chi2=r[0]; n=d['n']
    return dict(galaxy=name,model=model,chi2=chi2,bic=chi2+2*np.log(n),chi2red=chi2/(n-2))

def main():
    cat=pd.read_csv("../data/raw/sparc_sample123.csv")
    tasks=[(g,m) for m in ['nfw','burkert','einasto'] for g in cat['Galaxy']]
    with mp.Pool(18) as pool:
        rows=[r for r in pool.imap_unordered(fit_single,tasks) if r]
    sm=pd.DataFrame(rows)
    opp={m:sm[sm.model==m].set_index('galaxy') for m in ['nfw','burkert','einasto']}

    full=pd.read_csv("../data/tiered_spheres_full.csv")
    full['chi2_sphere']=full['chi2red_best']*(full['n_pts']-2*full['N_best'])
    full['bic_sphere']=full['bic_best']; full['N']=full['N_best']; full['cr_sphere']=full['chi2red_best']
    cap=pd.read_csv("../data/tiered_spheres_capped.csv")
    cap['chi2_sphere']=cap['chi2red_capped']*(cap['n_pts']-2*cap['N_capped'])
    cap['bic_sphere']=cap['chi2_sphere']+2*cap['N_capped']*np.log(cap['n_pts'])
    cap['N']=cap['N_capped']; cap['cr_sphere']=cap['chi2red_capped']

    def nbin(n): return '1 sphere' if n==1 else ('2 spheres' if n==2 else '3+ spheres')
    def grid(df,setlabel):
        df=df.copy(); df['bin']=df['N'].map(nbin)
        for score in ['BIC','chi2_red']:
            print(f"\n===== {setlabel}  |  scored by {score}  =====")
            print(f"  (cell = sphere WINS / LOSSES / TIES; tie band 2 BIC; 1sph-vs-Burkert N/A=same model)")
            print(f"  {'sphere count':12s} {'vs NFW':>12s} {'vs Burkert':>12s} {'vs Einasto':>12s}   {'galaxies':>8s}")
            for b in ['1 sphere','2 spheres','3+ spheres']:
                sub=df[df['bin']==b]
                if len(sub)==0: continue
                cells=[]
                for m in ['nfw','burkert','einasto']:
                    o=opp[m]
                    sc_s = sub['bic_sphere'].values if score=='BIC' else sub['cr_sphere'].values
                    sc_o = np.array([o.loc[g,'bic' if score=='BIC' else 'chi2red'] if g in o.index else np.nan for g in sub['galaxy']])
                    valid=~np.isnan(sc_o)
                    band=2.0 if score=='BIC' else 0.02
                    diff=sc_o[valid]-sc_s[valid]          # >0 = sphere better
                    wins=int(np.sum(diff> band)); losses=int(np.sum(diff<-band))
                    tie=int(np.sum(np.abs(diff)<=band)); tot=int(valid.sum())
                    # degenerate cell: 1-sphere vs Burkert IS the same model -> N/A
                    if b=='1 sphere' and m=='burkert':
                        cells.append("  N/A(=) ")
                    else:
                        cells.append(f"{wins}/{losses}/{tie}")
                print(f"  {b:12s} {cells[0]:>12s} {cells[1]:>12s} {cells[2]:>12s}   {len(sub):8d}")
            # totals
            sc_s=df['bic_sphere'].values if score=='BIC' else df['cr_sphere'].values
            line=[]; band=2.0 if score=='BIC' else 0.02
            for m in ['nfw','burkert','einasto']:
                o=opp[m]; sc_o=np.array([o.loc[g,'bic' if score=='BIC' else 'chi2red'] if g in o.index else np.nan for g in df['galaxy']])
                v=~np.isnan(sc_o); diff=sc_o[v]-sc_s[v]
                w=int(np.sum(diff>band)); l=int(np.sum(diff<-band)); t=int(np.sum(np.abs(diff)<=band))
                line.append(f"{w}/{l}/{t}")
            print(f"  {'ALL':12s} {line[0]:>14s} {line[1]:>14s} {line[2]:>14s}   {len(df):8d}")
    grid(full,"UNCAPPED sphere composite")
    grid(cap ,"CAPPED sphere composite")
if __name__=="__main__":
    mp.set_start_method("spawn",force=True); main()
