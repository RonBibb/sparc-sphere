"""Fig 2 (letter): shell-crossover radial concordance (capped two-domain, n=28).
Reproduces v0.7: Spearman rho=0.73 (p<1e-4), partial rho=0.62 controlling Reff."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import stats
m=pd.read_csv("../data/spatial_coincidence_capped.csv")
rho,p=stats.spearmanr(m.r_cross,m.r_shell)
def resid_on(y,x):
    ry=stats.rankdata(y); rx=stats.rankdata(x); b=np.polyfit(rx,ry,1); return ry-np.polyval(b,rx)
pr,_=stats.spearmanr(resid_on(m.r_cross,m.reff),resid_on(m.r_shell,m.reff))

plt.rcParams.update({"font.size":11,"axes.linewidth":0.8})
fig,ax=plt.subplots(figsize=(5.6,5.4))
lim=[0.8,45]
ax.plot(lim,lim,'-',color='0.6',lw=1.2,zorder=1,label='1:1')
ax.scatter(m.r_shell,m.r_cross,s=46,color='#1f6fb4',edgecolor='k',linewidth=0.6,zorder=4)
ax.set_xscale('log'); ax.set_yscale('log'); ax.set_xlim(lim); ax.set_ylim(lim)
ax.set_xlabel('shell radius $r_s$ (kpc)')
ax.set_ylabel('domain crossover radius $r_\\times$ (kpc)')
ax.set_title('Shell--crossover radial concordance',fontsize=11.5,fontweight='bold')
ax.set_aspect('equal'); ax.grid(alpha=0.22,which='both')
txt=(f'$n = {len(m)}$\n'
     f'Spearman $\\rho = {rho:.2f}$  ($p < 10^{{-4}}$)\n'
     f'partial $\\rho = {pr:.2f}$  (control $R_{{\\rm eff}}$)')
ax.text(0.04,0.96,txt,transform=ax.transAxes,va='top',ha='left',fontsize=9.5,
        bbox=dict(boxstyle='round,pad=0.45',fc='white',ec='0.7',alpha=0.95))
ax.legend(loc='lower right',fontsize=9,framealpha=0.95)
from matplotlib.ticker import FuncFormatter
for a in (ax.xaxis,ax.yaxis):
    a.set_major_formatter(FuncFormatter(lambda v,_:f'{v:g}'))
    a.set_minor_formatter(FuncFormatter(lambda v,_:''))
plt.tight_layout()
out="../figures/fig2_concordance.png"; plt.savefig(out,dpi=240,bbox_inches='tight')
print("SAVED",out)
print(f"VERIFY n={len(m)} rho={rho:.3f} partial={pr:.3f}")
