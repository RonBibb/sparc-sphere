import numpy as np, tiered_spheres as ts
rng=np.random.default_rng(7)
d=ts.load("NGC2403")
cand=ts.best_tiers(d,4,20,rng)
byN={N:(bic,chi2,th) for (bic,chi2,N,th) in cand}
print("NGC2403  n=%d  rmax=%.2f kpc"%(d['n'],d['rmax']))
for N in sorted(byN):
    bic,chi2,th=byN[N]
    print("  N=%d  BIC=%.2f  chi2=%.2f  chi2_red=%.2f"%(N,bic,chi2,chi2/(d['n']-2*N)))
if 1 in byN and 2 in byN:
    print("  dBIC(N1 - N2) = %.2f"%(byN[1][0]-byN[2][0]))
if 2 in byN:
    th=byN[2][2]; comps=ts.unpack(th,2)
    rr=np.linspace(d['r'].min(),d['rmax'],2000)
    (p0a,aa),(p0b,ab)=comps
    va=ts.v2_burk(rr,p0a,aa); vb=ts.v2_burk(rr,p0b,ab)
    cross=np.where(np.diff(np.sign(va-vb)))[0]
    print("  comps: inner a=%.2f logrho0=%.2f | outer a=%.2f logrho0=%.2f"%(aa,p0a,ab,p0b))
    print("  crossover (v2 equal): %s kpc"%(", ".join("%.2f"%rr[c] for c in cross) if len(cross) else "none"))
