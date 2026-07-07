import sys, numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
GEO={ # dB08 Table 2 (RA, Dec sexagesimal; D Mpc; Vsys; inc; PA)
 'NGC_2841': ("09:22:02.6","+50:58:35.4",14.1,633.7,73.7,152.6),
 'NGC_3198': ("10:19:55.0","+45:32:58.9",13.8,660.7,71.5,215.0),
 'NGC_3521': ("11:05:48.6","-00:02:09.2",10.7,803.5,72.7,339.8),
}
g=sys.argv[1]; ra,dec,D,vsys,inc,pa=GEO[g]
cube=f"{g}_RO_CUBE_THINGS.FITS"
h=fits.getheader(cube)
w=WCS(h).celestial
c=SkyCoord(ra,dec,unit=(u.hourangle,u.deg))
x,y=w.world_to_pixel(c)
par=f"""FITSFILE    {cube}
THREADS     6
3DFIT       true
NRADII      25
RADSEP      30
VSYS        {vsys}
XPOS        {x:.1f}
YPOS        {y:.1f}
VROT        150
VDISP       10
INC         {inc}
PA          {pa}
Z0          10
FREE        VROT VDISP PA
LTYPE       2
FTYPE       2
DISTANCE    {D}
MASK        SEARCH
WFUNC       2
TWOSTAGE    true
OUTFOLDER   out_{g}
"""
open(f"{g.lower()}.par","w").write(par)
print(f"{g}: center pix ({x:.1f},{y:.1f}); par written")
