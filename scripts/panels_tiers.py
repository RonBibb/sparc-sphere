import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import warnings; warnings.filterwarnings("ignore")
import tiered_spheres as ts

df=pd.read_csv("../data/processed/tiered_spheres_full.csv")
n3=df[df.N_best==3].sort_values('dBIC',ascending=False)['galaxy'].tolist()[:5]
n2=df[(df.N_best==2)&(df.n_pts>=20)].sort_values('dBIC',ascending=False)['galaxy'].tolist()[:5]
print("N=2 panels:",n2); print("N=3 panels:",n3)
cols=["#2ca02c","#ff7f0e","#9467bd"]

fig,ax=plt.subplots(5,2,figsize=(14,19))
def panel(a,g):
    d=ts.load(g); rng=np.random.default_rng(7)
    cands=ts.best_tiers(d,4,20,rng); byN={c[2]:c for c in cands}
    bicB,chiB,NB,thB=cands[0]; _,_,_,th1=byN[1]
    rr=np.linspace(d['r'].min(),d['rmax'],500); v2b=np.interp(rr,d['r'],d['v2b'])
    a.errorbar(d['r'],d['vo'],yerr=d['ev'],fmt='o',ms=3.3,color='k',ecolor='0.6',capsize=1.5,zorder=6,label='V_obs')
    a.plot(rr,np.sqrt(np.maximum(v2b,0)),':',color='0.5',lw=1.3,label='baryons')
    # single-Burkert backbone reference
    p0b,ab=ts.unpack(th1,1)[0]
    a.plot(rr,np.sqrt(np.maximum(v2b+ts.v2_burk(rr,p0b,ab),0)),'-',color='#8c564b',lw=1.4,alpha=0.9,label='single Burkert (1 sphere)')
    # individual spheres (bare contribution) + composite
    v2tot=v2b.copy()
    for j,(p0,asc) in enumerate(ts.unpack(thB,NB)):
        vc=ts.v2_burk(rr,p0,asc); v2tot=v2tot+vc
        a.plot(rr,np.sqrt(np.maximum(vc,0)),'--',color=cols[j],lw=1.5,label=f'sphere {j+1} (a={asc:.1f})')
    a.plot(rr,np.sqrt(np.maximum(v2tot,0)),'-',color='#1f6fb4',lw=2.4,label=f'composite total (N={NB})')
    cr=chiB/(d['n']-2*NB)
    a.set_title(f"{g}  —  N={NB} spheres,  χ²_red={cr:.2f}",fontsize=10,fontweight='bold')
    a.set_xlabel("r (kpc)"); a.set_ylabel("V (km/s)"); a.grid(alpha=0.25); a.legend(fontsize=6.5,loc='lower right')

for i in range(5):
    panel(ax[i,0], n2[i])
    panel(ax[i,1], n3[i])
ax[0,0].text(0.5,1.18,"BIC-selected 2 spheres",transform=ax[0,0].transAxes,ha='center',fontsize=12,fontweight='bold',color='#1f6fb4')
ax[0,1].text(0.5,1.18,"BIC-selected 3 spheres",transform=ax[0,1].transAxes,ha='center',fontsize=12,fontweight='bold',color='#9467bd')
plt.tight_layout(rect=[0,0,1,0.985])
plt.savefig("../panels_tiers_2and3.png",dpi=130,bbox_inches="tight")
print("saved panels_tiers_2and3.png")
