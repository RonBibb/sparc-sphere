# Cross-match van den Bosch 2016 measured-MBH compilation against the capped sample.
# Then: baseline test on CLEAN single-sphere galaxies (exclude the 8 borderline
# penalty-blocked singles): measured logMBH vs fitted DM halo mass.
import numpy as np, pandas as pd, warnings, re
from astropy.io import fits
from astropy.table import Table
from scipy import stats
warnings.filterwarnings("ignore")
import tiered_spheres as ts, tiered_spheres_capped as tc

t=Table.read("../data/raw/BHcompilation_vdB16.fits").to_pandas()
print("vdB16 columns:",list(t.columns)[:12]); print(f"vdB16 rows: {len(t)}")
namecol=[c for c in t.columns if c.lower() in ('name','galaxy','gal')][0]
def norm(n):
    n=str(n).strip().upper().replace(' ','')
    m=re.match(r'(NGC|UGC|IC|DDO)0*(\d+)(.*)',n)
    return f"{m.group(1)}{int(m.group(2))}{m.group(3)}" if m else n
t['key']=[norm(x.decode() if isinstance(x,bytes) else x) for x in t[namecol]]

cap=pd.read_csv("../data/tiered_spheres_capped.csv")
F=pd.read_csv("../data/forced_two_sphere.csv")
borderline=set(F[(F.group=='forced')&(F.dchi2>2)].galaxy)  # the 8 penalty-blocked
cap['key']=[norm(g) for g in cap.galaxy]
m=cap.merge(t,on='key',how='inner')
print(f"\nSPARC capped sample x vdB16 measured-MBH matches: {len(m)}")
if len(m):
    bh=[c for c in t.columns if 'bh' in c.lower() or 'mbh' in c.lower()]
    print("BH cols:",bh)
    for _,r in m.iterrows():
        cls='WINNER (N>=2)' if r.N_capped>=2 else ('borderline single' if r.galaxy in borderline else 'clean single')
        print(f"  {r.galaxy:10s} {cls}")
m.to_csv("../data/vdb16_sparc_matches.csv",index=False)
print("saved data/vdb16_sparc_matches.csv")
