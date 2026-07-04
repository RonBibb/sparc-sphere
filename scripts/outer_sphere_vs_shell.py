# Treat the outer sphere of each capped 2-domain galaxy as if it were a "shell":
# compare to the relaxed shell sweep's actual shell at that location.
# Three axes: LOCATION (peak of outer sphere's dM/dr vs shell radius),
#             MASS (outer sphere enclosed mass within data vs shell mass),
#             WIDTH (FWHM of outer sphere's mass distribution vs shell FWHM).
import numpy as np, pandas as pd
from scipy import stats
import sys; sys.path.insert(0,".")
import tiered_spheres as ts

W=pd.read_csv("../data/forced_two_sphere.csv")
W=W[W.group=='winner'].copy()
sh=pd.read_csv("../data/raw/shell_model_sweep_shells.csv")
sh=sh[(sh.model=='burkert')&(np.isclose(sh.cap,0.4))&(sh.shell_idx>0)].copy()
for c in ['r_kpc','M_Msun','sigma_kpc']: sh[c]=pd.to_numeric(sh[c],errors='coerce')

rows=[]
for _,x in W.iterrows():
    g=x.galaxy; sg=sh[sh.galaxy==g]
    if len(sg)==0: continue
    rr=np.linspace(0.05,x.rmax,3000)
    # outer sphere mass distribution dM/dr = 4 pi r^2 rho(r)
    rho=10**x.p0_out/((1+rr/x.a_out)*(1+(rr/x.a_out)**2))
    dMdr=4*np.pi*rr**2*rho
    ipk=np.argmax(dMdr); r_pk=rr[ipk]
    half=dMdr>=0.5*dMdr[ipk]
    fwhm_sphere=rr[half][-1]-rr[half][0]   # within data window (truncated if peak at edge)
    truncated=bool(half[-1])               # still above half-max at r_max
    M_outer=ts.M_burk(x.rmax,x.p0_out,x.a_out)
    # nearest shell (to dM/dr peak) and OUTERMOST shell
    j=np.argmin(np.abs(sg.r_kpc.values-r_pk)); s=sg.iloc[j]
    rows.append(dict(galaxy=g,r_pk=r_pk,r_shell=s.r_kpc,rmax=x.rmax,
        M_outer=M_outer,M_shell=s.M_Msun,massratio=M_outer/max(s.M_Msun,1),
        fwhm_sphere=fwhm_sphere,fwhm_shell=2.355*s.sigma_kpc,
        widthratio=fwhm_sphere/max(2.355*s.sigma_kpc,1e-3),truncated=truncated))
m=pd.DataFrame(rows); m.to_csv("../data/outer_sphere_vs_shell.csv",index=False)
print(f"two-domain galaxies with shells: n={len(m)}\n")
print("LOCATION — outer-sphere dM/dr peak vs shell radius")
rho_,p_=stats.spearmanr(m.r_pk,m.r_shell)
print(f"  Spearman rho={rho_:.2f} (p={p_:.1e});  median |offset|/rmax={np.median(np.abs(m.r_pk-m.r_shell)/m.rmax):.3f}")
print(f"  (note: {int(m.truncated.sum())}/{len(m)} outer spheres still above half-max at r_max -> width/peak truncated by data edge)\n")
print("MASS — outer sphere enclosed (within data) vs shell mass")
print(f"  median M_outer = {m.M_outer.median():.2e}  median M_shell = {m.M_shell.median():.2e}")
print(f"  median ratio M_outer/M_shell = {m.massratio.median():.1f}x   16-84%: {m.massratio.quantile(.16):.1f}-{m.massratio.quantile(.84):.1f}x")
r2,p2=stats.spearmanr(np.log10(m.M_outer),np.log10(m.M_shell))
print(f"  do they CORRELATE? Spearman rho={r2:.2f} (p={p2:.4f})\n")
print("WIDTH — FWHM of outer-sphere mass distribution vs shell FWHM")
print(f"  median FWHM_sphere = {m.fwhm_sphere.median():.1f} kpc   FWHM_shell = {m.fwhm_shell.median():.1f} kpc")
print(f"  median width ratio = {m.widthratio.median():.1f}x broader")
