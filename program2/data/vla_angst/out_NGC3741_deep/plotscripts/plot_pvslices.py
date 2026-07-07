#######################################################################
#### This script writes a plot of P-V slices across several cuts   ####
#######################################################################
import numpy as np 
import os 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from plot_utils import *
from astropy.io import fits 
from astropy.visualization import ImageNormalize, PercentileInterval, PowerStretch

labsize = 13
mpl.rc('xtick',direction='in',top=True) 
mpl.rc('ytick',direction='in',right=True) 
mpl.rcParams['contour.negative_linestyle'] = 'solid' 
plt.rc('font',family='sans-serif',serif='Helvetica',size=labsize) 
params = {'text.usetex': False, 'mathtext.fontset': 'cm', 'mathtext.default': 'regular'} 
plt.rcParams.update(params) 

gname = 'NGC3741' 
outfolder = 'out_NGC3741_deep/' 
outprefix = 'NGC3741' 
twostage = 1 
plotmask = 0 

image = fits.open('NGC3741-nat-cube.fits') 
image_mas = fits.open(outfolder+'mask.fits') 
xmin, xmax = 264, 754
ymin, ymax = 271, 761
zmin, zmax = 6, 110
zmin_wcs, zmax_wcs = 161.28, 296.751
data = image[0].data[0,zmin:zmax+1,ymin:ymax+1,xmin:xmax+1] 
data_mas = image_mas[0].data[zmin:zmax+1,ymin:ymax+1,xmin:xmax+1] 
zsize, ysize, xsize = data.shape 
pad_x, pad_y = calculate_padding(xsize,ysize) 
cdeltsp=1.5
cont = 0.00191498
v = np.array([1,2,4,8,16,32,64])*cont 
v_neg = [-cont] 
mom0 = fits.open(outfolder+'/maps/'+outprefix+'_0mom.fits')[0].data[ymin:ymax+1,xmin:xmax+1] 
mom0p = np.pad(mom0,(pad_y, pad_x),mode='constant',constant_values=np.nan) 
extm = [0,mom0p.shape[1]-1,0,mom0p.shape[0]-1]
norm = ImageNormalize(data, interval=PercentileInterval(99.9), stretch=PowerStretch(1.0))
norm0 = ImageNormalize(mom0, interval=PercentileInterval(99.0), stretch=PowerStretch(0.5))

frile = outfolder + ('rings_final2.txt' if twostage else 'rings_final1.txt')
rings = np.genfromtxt(frile,usecols=(1,2,3,4,5,9,10,11),unpack=True)
rad,vrot,vdisp,inc,pa,xpos,ypos,vsys = rings
xcen_m,ycen_m,vsys_m,inc_m,pa_m = np.nanmean((xpos,ypos,vsys,inc,pa),axis=1) 
xcen_m,ycen_m = xcen_m-xmin, ycen_m-ymin 
proj_vmax = np.nanmax(vrot)*np.sin(np.radians(inc_m))
max_vdisp = np.nanmax(vdisp)

s_maj,x_maj,y_maj = build_path(xcen_m, ycen_m, rad/cdeltsp, np.full(len(rad),pa_m), xsize, ysize)
s_min,x_min,y_min = build_path(xcen_m, ycen_m, rad/cdeltsp, np.full(len(rad),pa_m+90), xsize, ysize)
s_maj = s_maj*cdeltsp
s_min = s_min*cdeltsp
maj_offsets = np.linspace(0,rad[-1],3,endpoint=True)
min_offsets = np.linspace(0,rad[-1]*np.cos(np.radians(inc_m)),3,endpoint=True)
maj_offsets = np.concatenate([-maj_offsets[1:][::-1],maj_offsets,])
min_offsets = np.concatenate([-min_offsets[1:][::-1],min_offsets,])
x_maj_s = np.interp(min_offsets, s_min, x_min)
y_maj_s = np.interp(min_offsets, s_min, y_min)
x_min_s = np.interp(maj_offsets, s_maj, x_maj)
y_min_s = np.interp(maj_offsets, s_maj, y_maj)

files_mod = [f for f in sorted(os.listdir(outfolder)) if outprefix+'mod' in f] 
if len(files_mod)==0: raise FileNotFoundError('ERROR: no model in output directory') 

cmap = plt.cm.PuBu_r 
colors = cmap(np.linspace(0, 1, 13)) 


def plot_pv(i,ax,ax_m,x0,y0,theta,**kwargs):

  s,x,y = build_path(x0, y0, rad/cdeltsp, np.full(len(rad),theta), xsize, ysize)
  pv_data = extract_pv(data,x,y)
  pv_mod  = extract_pv(data_mod,x,y)
  s_arcsec = s * cdeltsp
  ext = [s_arcsec[0], s_arcsec[-1], zmin_wcs-vsys_m,zmax_wcs-vsys_m]

  ax.imshow(pv_data,origin='lower',cmap='Blues',norm=norm,aspect='auto',interpolation='nearest',extent=ext)
  ax.contour(pv_data,v,origin='lower',linewidths=0.7,colors='#00008B',extent=ext) 
  ax.contour(pv_data,v_neg,origin='lower',linewidths=0.1,colors='gray',extent=ext) 
  ax.contour(pv_mod,v,origin='lower',linewidths=1.2,colors='#B22222',extent=ext) 
  ax.axhline(y=0,color='black') 
  ax.axvline(x=0,color='black') 
  ax.grid(color='gray', linestyle='--', linewidth=0.3) 

  if plotmask:
    pv_mask = extract_pv(data_mas,x,y) 
    ax.contour(pv_mask,levels=[0],origin='lower',linewidths=1.5,colors='k',extent=ext)

  ax.set_xlim(-1.3*rad[-1],1.3*rad[-1])
  #ax.set_ylim(-1.1*(proj_vmax+2*max_vdisp),1.1*(proj_vmax+2*max_vdisp))
  ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=5))
  ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=5))
  if i==0 or i==5: 
    ax.tick_params(labelbottom=True,labelleft=True)
    ax.set_ylabel(r'$\mathrm{\Delta V_{LOS}}$ (km/s)',fontsize=labsize+2) 
  else: ax.tick_params(labelbottom=True,labelleft=False)
  ax.set_xlabel('Offset (arcsec)',fontsize=labsize)
  ax_m.plot(x+pad_x[0],y+pad_y[0],**kwargs) 

# Beginning position-velocity plot 
for k in range (len(files_mod)): 
  image_mod = fits.open(outfolder+files_mod[k]) 
  data_mod = image_mod[0].data[zmin:zmax+1,ymin:ymax+1,xmin:xmax+1]

  fig, axes = defineaxis(4,5,0.3,0.3,xsep=0.01,ysep=0.1,fig_width=10,fig_heigth=10)
  axes = np.ravel(axes)

  pos = axes[4].get_position()
  ax_m1 = fig.add_axes([pos.x1+0.03,pos.y0-0.2,0.3,0.3])
  pos = axes[14].get_position()
  ax_m2 = fig.add_axes([pos.x1+0.03,pos.y0-0.2,0.3,0.3])

  # Plotting moment map
  pm = np.pad(mom0,(pad_y, pad_x),mode='constant',constant_values=np.nan) 
  for ax in [ax_m1,ax_m2]:
    ax.set_prop_cycle(color=colors)
    ax.tick_params(labelbottom=False,labelleft=False,top=False,bottom=False,left=False,right=False)
    ax.imshow(pm,origin='lower',cmap='Greys',aspect='auto',interpolation='nearest',norm=norm0,extent=extm)
    ax.set_title('Slices')
    ax.plot(xcen_m+pad_x[0],ycen_m+pad_y[0],'x',color='yellow',markersize=7,mew=1.5,zorder=12) 
    ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=5))
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=5))

  pos = ax_m2.get_position()
  ax_m2.set_position([pos.x0,pos.y0 - 0.07,pos.width,pos.height])

  dtheta = 18
  for i,ax in enumerate(axes[0:10]):
    theta = pa_m + i*dtheta  
    ls = 'solid' if i<5 else 'dashed'
    plot_pv(i,ax,ax_m1,xcen_m,ycen_m,theta,ls=ls,label=rf'{i*dtheta:.0f}$^\circ$')
    ax.text(0.03,1.03,rf"$\theta$ = {i*dtheta:.0f}$^\circ$",transform=ax.transAxes,fontsize=labsize)
    theta += 15.

  for i,ax in enumerate(axes[10:]):
    pos = ax.get_position()
    ax.set_position([pos.x0,pos.y0 - 0.05,pos.width,pos.height])

    if i<5:
      xi,yi,off,theta = x_maj_s[i],y_maj_s[i],min_offsets[i],pa_m
      ls = 'solid'
    else:
      xi,yi,off,theta = x_min_s[i-5],y_min_s[i-5],maj_offsets[i-5],pa_m + 90
      ls = 'dashed'

    plot_pv(i,ax,ax_m2,xi,yi,theta,ls=ls,label=rf"{off:.1f}''")
    ax.text(0.03,1.03,rf"offset = {off:.1f}''",transform=ax.transAxes,fontsize=labsize)
    ax_m2.plot(xi+pad_x[0],yi+pad_y[0],'o',c='royalblue',zorder=11)
  leg_opts = dict(ncol=2,loc='upper left',bbox_to_anchor=(0.0, -0.05),frameon=False)
  ax_m1.legend(**leg_opts,handlelength=3.3)
  ax_m2.legend(**leg_opts,handlelength=2)

  outfile = '%s_pvslices'%outprefix 
  ntype   = files_mod[k][files_mod[k].rfind('_'):].replace('.fits','') 
  fig.savefig(outfolder+outfile+ntype+'.pdf', bbox_inches='tight') 
  image_mod.close() 

image.close() 
image_mas.close() 
