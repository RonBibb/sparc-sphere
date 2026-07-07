#################################################################################
#### This script writes a plot of position-velocity slices of model and data ####
#################################################################################
import numpy as np 
import os 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from plot_utils import *
from astropy.io import fits 
from astropy.visualization import ImageNormalize, PercentileInterval, PowerStretch

labsize = 18
mpl.rc('xtick',direction='in',top=True) 
mpl.rc('ytick',direction='in',right=True) 
mpl.rcParams['contour.negative_linestyle'] = 'solid' 
plt.rc('font',family='sans-serif',serif='Helvetica',size=labsize) 
params = {'text.usetex': False, 'mathtext.fontset': 'cm', 'mathtext.default': 'regular'} 
plt.rcParams.update(params) 

gname = 'NGC3741' 
outfolder = 'out_NGC3741/' 
outprefix = 'NGC3741' 
twostage = 1 
plotmask = 0 

image = fits.open('NGC3741-nat-cube.fits') 
image_mas = fits.open(outfolder+'mask.fits') 
xmin, xmax = 305, 713
ymin, ymax = 312, 720
zmin, zmax = 8, 104
zmin_wcs, zmax_wcs = 163.859, 289.006
data = image[0].data[0,zmin:zmax+1,ymin:ymax+1,xmin:xmax+1] 
data_mas = image_mas[0].data[zmin:zmax+1,ymin:ymax+1,xmin:xmax+1] 
zsize, ysize, xsize = data.shape 
pad_x, pad_y = calculate_padding(xsize,ysize) 
cdeltsp=1.5
cont = 0.00239373
v = np.array([1,2,4,8,16,32,64])*cont 
v_neg = [-cont] 
mom0 = fits.open(outfolder+'/maps/'+outprefix+'_0mom.fits')[0].data[ymin:ymax+1,xmin:xmax+1] 
mom1 = fits.open(outfolder+'/maps/'+outprefix+'_1mom.fits')[0].data[ymin:ymax+1,xmin:xmax+1] 
mom0p = np.pad(mom0,(pad_y, pad_x),mode='constant',constant_values=np.nan) 
mom1p = np.pad(mom1,(pad_y, pad_x),mode='constant',constant_values=np.nan) 
extm = [0,mom0p.shape[1]-1,0,mom0p.shape[0]-1]
norm0 = ImageNormalize(mom0, interval=PercentileInterval(98.0), stretch=PowerStretch(0.5))
norm1 = ImageNormalize(mom1, interval=PercentileInterval(99.5))

frile = outfolder + ('rings_final2.txt' if twostage else 'rings_final1.txt')
rings = np.genfromtxt(frile,usecols=(1,2,3,4,5,9,10,11),unpack=True)
rad,vrot,vdisp,inc,pa,xpos,ypos,vsys = rings
xcen_m,ycen_m,vsys_m,inc_m,pa_m = np.nanmean((xpos,ypos,vsys,inc,pa),axis=1) 
xcen_m, ycen_m = xcen_m-xmin, ycen_m-ymin 
proj_vmax = np.nanmax(vrot)*np.sin(np.radians(inc_m))
max_vdisp = np.nanmax(vdisp)
radii = np.concatenate((rad,-rad)) 
vlos1 = vrot*np.sin(np.deg2rad(inc))
vlos = np.concatenate((vlos1,-vlos1)) 

files_mod = [f for f in sorted(os.listdir(outfolder)) if outprefix+'mod' in f] 
if len(files_mod)==0: raise FileNotFoundError('ERROR: no model in output directory') 


def plot_pv(ax,x0,y0,theta,**kwargs):

  s,x,y = build_path(x0, y0, rad/cdeltsp, theta, xsize, ysize)
  pv_data = extract_pv(data,x,y,order=0)
  pv_mod  = extract_pv(data_mod,x,y)
  norm = ImageNormalize(vmin=cont, vmax=np.percentile(data, 99.8), stretch=PowerStretch(0.5)) 
  #norm = ImageNormalize(data, interval=PercentileInterval(99.9), stretch=PowerStretch(1.0))

  s_arcsec = s * cdeltsp
  ext = [s_arcsec[0], s_arcsec[-1], zmin_wcs-vsys_m,zmax_wcs-vsys_m]

  ax.imshow(pv_data,origin='lower',cmap='Greys',norm=norm,aspect='auto',interpolation='nearest',extent=ext)
  ax.contour(pv_data,v,origin='lower',linewidths=1.0,colors='#00008B',extent=ext) 
  ax.contour(pv_data,v_neg,origin='lower',linewidths=0.2,colors='gray',extent=ext) 
  ax.contour(pv_mod,v,origin='lower',linewidths=1.5,colors='#B22222',extent=ext) 
  ax.axhline(y=0,color='black') 
  ax.axvline(x=0,color='black') 
  ax.grid(color='gray', linestyle='--', linewidth=0.3) 

  if plotmask:
    pv_mask = extract_pv(data_mas,x,y) 
    ax.contour(pv_mask,levels=[0],origin='lower',linewidths=3.5,colors='k',extent=ext)

  ax.set_xlim(-1.3*rad[-1],1.3*rad[-1])
  #ax.set_ylim(-1.1*(proj_vmax+2*max_vdisp),1.1*(proj_vmax+2*max_vdisp))
  ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=6))
  ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=6))
  ax.tick_params(labelbottom=True,labelleft=True)
  ax.tick_params(which='major',length=8, labelsize=labsize) 
  ax.set_ylabel(r'$\mathrm{\Delta V_{LOS}}$ (km/s)',fontsize=labsize+2) 
  ax.set_xlabel('Offset (arcsec)',fontsize=labsize+2)

  ax2 = ax.twinx()
  ax2.set_ylim([ext[2]+vsys_m,ext[3]+vsys_m]) 
  ax2.tick_params(which='major',length=8, labelsize=labsize) 
  ax2.set_ylabel(r'$\mathrm{V_{LOS}}$ (km/s)',fontsize=labsize+2) 

  return s,x,y


# Beginning position-velocity plot
for k in range (len(files_mod)): 
  image_mod = fits.open(outfolder+files_mod[k]) 
  data_mod = image_mod[0].data[zmin:zmax+1,ymin:ymax+1,xmin:xmax+1]

  fig, axes = defineaxis(2,1,1,0.7,xsep=0,ysep=0.1,fig_width=9,fig_heigth=9)
  axes = np.ravel(axes)

  # Major axis
  s,x,y = plot_pv(axes[0],xcen_m,ycen_m,pa)
  axes[0].text(0, 1.05, gname, transform=axes[0].transAxes,fontsize=32) 

  fig.canvas.draw()
  renderer = fig.canvas.get_renderer() 
  bbox = axes[0].get_tightbbox(renderer).transformed(fig.transFigure.inverted())
  pos = axes[0].get_position()
  ax_m = fig.add_axes([bbox.x1+0.14,pos.y1-0.4,0.4,0.4])

  ax_m.tick_params(labelbottom=False,labelleft=False,top=False,bottom=False,left=False,right=False) 
  ax_m.imshow(mom0p,origin='lower',cmap='Greys',aspect='auto',interpolation='nearest',norm=norm0,extent=extm)
  ax_m.imshow(mom1p,origin='lower',cmap='seismic',aspect='auto',interpolation='nearest',norm=norm1,extent=extm, alpha=0.4)
  ax_m.plot(xcen_m+pad_x[0],ycen_m+pad_y[0],'x',color='y',markersize=7,mew=1.5,zorder=10)
  ax_m.annotate('',xy=(0.8,-0.1),xycoords='axes fraction',xytext=(1.0, -0.1),arrowprops=dict(arrowstyle='<->', color='k', lw=1.5))
  ax_m.text(0.9,-0.16,f"{0.2*xsize*cdeltsp:.0f}''",transform=ax_m.transAxes,fontsize=12, ha='center')
  ax_m.axvline(xcen_m+pad_x[0],ls='dotted',c='k',alpha=0.2)
  ax_m.axhline(ycen_m+pad_y[1],ls='dotted',c='k',alpha=0.2)
  _,ax_m_xmax = ax_m.get_xlim()
  _,ax_m_ymax = ax_m.get_ylim()
  m = (x >= 0) & (x < ax_m_xmax) & (y >= 0) & (y < ax_m_ymax)
  ax_m.plot(x[m]+pad_x[0],y[m]+pad_y[0],'-',lw=1.5,c='#B22222') 
  ax_m.plot(x[~m]+pad_x[0],y[~m]+pad_y[0],'-',lw=1.5,c='#B22222',alpha=0.3) 

  # Plotting rotation curve 
  r = np.sqrt((x-xcen_m)**2+(y-ycen_m)**2)
  r[s<0] *= -1
  x_rad = np.interp(radii/cdeltsp,r,x)
  y_rad = np.interp(radii/cdeltsp,r,y)
  s_rad = np.interp(radii/cdeltsp,r,s)
  axes[0].plot(s_rad*cdeltsp,vlos,'o',c='gold',ms=10,alpha=0.8,mec='cornsilk') 
  ax_m.scatter(x_rad+pad_x[0],y_rad+pad_y[0],c='gold',s=10,alpha=0.8) 

  # Minor axis
  s,x,y = plot_pv(axes[1],xcen_m,ycen_m,pa+90)
  m = (x >= 0) & (x < ax_m_xmax) & (y >= 0) & (y < ax_m_ymax)
  ax_m.plot(x[m]+pad_x[0],y[m]+pad_y[0],'--',lw=1.5,c='navy') 
  ax_m.plot(x[~m]+pad_x[0],y[~m]+pad_y[0],'--',lw=1.5,c='navy',alpha=0.3) 

  xran_min = rad[-1]*np.sin(np.radians(inc_m))
  axes[1].set_xlim(-1.3*xran_min,1.3*xran_min)

  outfile = '%s_pv'%outprefix
  ntype   = files_mod[k][files_mod[k].rfind('_'):].replace('.fits','') 
  fig.savefig(outfolder+outfile+ntype+'.pdf', bbox_inches='tight') 
  image_mod.close() 

image.close() 
image_mas.close() 
