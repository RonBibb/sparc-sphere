# Build DiskFit .inp files for NGC 2841 from the THINGS MOM1 map + dB08 Table 2 geometry.
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u

MOM1 = "../../../data/things_pilot/NGC_2841_RO_MOM1_THINGS.FITS"
RA, DEC = "09:22:02.6", "+50:58:35.4"     # dB08 Table 2
VSYS, INC, PA = 633.7, 73.7, 152.6        # dB08 Table 2
PIXSCALE = 1.5                             # THINGS ''/pix
RING_STEP_PIX, RING_MAX_PIX = 10, 320      # rings every 15'' out to ~345''
NBOOT = 200                                # bootstrap realizations (raise to 1000 for final)

h = fits.getheader(MOM1)
w = WCS(h).celestial
c = SkyCoord(RA, DEC, unit=(u.hourangle, u.deg))
x, y = w.world_to_pixel(c)
nx, ny = h["NAXIS1"], h["NAXIS2"]
eps = 1 - np.cos(np.radians(INC))
rings = "\n".join(f"{r:.1f}" for r in range(RING_STEP_PIX, RING_MAX_PIX + 1, RING_STEP_PIX))

def inp(name, boot):
    return f"""NGC2841 THINGS MOM1, dB08 geometry # pixscale {PIXSCALE}''/pix
vels                               # vels/phot switch
T  T                               # FITS I/O, vels in m/s
'{MOM1}'                           # input velocity field
None                               # velocity uncertainty map
1  1  {nx} {ny}                    # region: (xlow,ylow) & (xrange,yrange)
12.0  {PA:.2f}  {eps:.3f}  6 {PIXSCALE} # regrad, regpa, regeps, istepout, pixscale
'OUT_2841/{name}.out'              # output file
T T T                              # fit PA, eps & center
{PA:.2f}  {eps:.3f}                # initial PA, eps
{x:.1f}  {y:.1f}                   # initial center (pix)
F F 0.0 2                          # non-circular flow OFF (disk-only)
T F                                # inner interpolation, radial flows
T {VSYS:.1f} 1.0 25.0              # fit Vsys, initial Vsys, delta_ISM, errtol
F F F F 90 0 0                     # warp OFF
0.                                 # seeing correction
-0.01 -0.01                        # smoothing lambdas
{'T' if boot else 'F'} -50 {NBOOT} -1.0   # UNCERTAINTIES: toggle, seed, nboot, junc
T                                  # verbose
3.0 0.0                            # min,max radii for noncirc (unused)
{rings}
"""

import os
os.makedirs("OUT_2841", exist_ok=True)
open("ngc2841_disk.inp", "w").write(inp("disk2841", False))
open("ngc2841_boot.inp", "w").write(inp("boot2841", True))
print(f"center pix: ({x:.1f},{y:.1f})  eps={eps:.3f}  rings: {RING_STEP_PIX}-{RING_MAX_PIX} pix")
print("wrote ngc2841_disk.inp (fast, no errors) and ngc2841_boot.inp (bootstrap)")
