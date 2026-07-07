#######################################################################
#### This script writes a plot of kinematic maps of model and data ####
#######################################################################
import numpy as np 
import os 
import matplotlib as mpl 
import matplotlib.pyplot as plt 
from matplotlib.colorbar import ColorbarBase 
from plot_utils import calculate_padding, defineaxis 
from astropy.io import fits 
from astropy.visualization import PercentileInterval 
from copy import copy 
mpl.rc('xtick',direction='in') 
mpl.rc('ytick',direction='in') 
plt.rc('font',family='sans-serif',serif='Helvetica',size=10) 
params = {'text.usetex': False, 'mathtext.fontset': 'cm', 'mathtext.default': 'regular'} 
plt.rcParams.update(params) 

gname = 'NGC3198' 
outfolder = 'out_NGC_3198/' 
outprefix = 'NGC3198' 
twostage = 1 
xmin, xmax = 151, 869
ymin, ymax = 152, 870

# Opening maps and retrieving intensity map units
f0 = fits.open(outfolder+'/maps/'+outprefix+'_0mom.fits') 
f1 = fits.open(outfolder+'/maps/'+outprefix+'_1mom.fits') 
f2 = fits.open(outfolder+'/maps/'+outprefix+'_2mom.fits') 
bunit = f0[0].header['BUNIT'] 
bunit = bunit.replace(' ', '').lower() 
# Now plotting moment maps 
mom0 = f0[0].data[ymin:ymax+1,xmin:xmax+1] 
mom1 = f1[0].data[ymin:ymax+1,xmin:xmax+1] 
mom2 = f2[0].data[ymin:ymax+1,xmin:xmax+1] 
maskmap = np.copy(mom1) 
maskmap[mom1==mom1] = 1 
ysize, xsize = mom0.shape 
pad_x, pad_y = calculate_padding(xsize,ysize) 

if twostage: rad,inc,pa,xpos,ypos,vsys = np.genfromtxt(outfolder+'rings_final2.txt',usecols=(1,4,5,9,10,11),unpack=True) 
else: rad,inc,pa,xpos,ypos,vsys = np.genfromtxt(outfolder+'rings_final1.txt',usecols=(1,4,5,9,10,11),unpack=True) 
xcen_m,ycen_m,inc_m,pa_m,vsys_m=np.nanmean((xpos,ypos,inc,pa,vsys),axis=1) 
xcen, ycen = xcen_m-xmin+pad_x[0], ycen_m-ymin+pad_y[0] 

files_mod0 = [f for f in sorted(os.listdir(outfolder+'maps/')) if outprefix+'mod_0mom' in f] 
files_mod1 = [f for f in sorted(os.listdir(outfolder+'maps/')) if outprefix+'mod_1mom' in f] 
files_mod2 = [f for f in sorted(os.listdir(outfolder+'maps/')) if outprefix+'mod_2mom' in f] 
if len(files_mod0)==0 or len(files_mod1)==0 or len(files_mod2)==0 : raise FileNotFoundError('ERROR: no model maps in output directory') 


cmaps = [plt.get_cmap('Spectral_r'),plt.get_cmap('coolwarm'),plt.get_cmap('PuOr_r')] 
barlab = ['Intensity ('+bunit+')', r'V$_\mathrm{LOS}$ (km/s)', r'$\sigma_\mathrm{obs}$ (km/s)'] 
barlab2 = [r'I$_\mathrm{res}$ ('+bunit+')', r'V$_\mathrm{res}$ (km/s)', r'$\sigma_\mathrm{res}$ (km/s)'] 
titles = ['DATA', 'MODEL','RESIDUALS'] 
mapname = ['MOMENT 0TH', 'MOMENT 1ST', 'MOMENT 2ND'] 
x = np.arange(0,xmax-xmin,0.1) 
y = np.tan(np.radians(pa_m-90))*(x-xcen)+ycen 
ext = [0,xmax-xmin+pad_x[0]+pad_x[1],0, ymax-ymin+pad_y[0]+pad_y[1]] 
rad_pix = rad/1.5
try: nr = len(rad_pix) 
except: nr = 1 
interval = PercentileInterval(99.5) 

for k in range (len(files_mod0)): 
  mom0_mod = fits.open(outfolder+'/maps/'+files_mod0[k])[0].data[ymin:ymax+1,xmin:xmax+1] 
  mom1_mod = fits.open(outfolder+'/maps/'+files_mod1[k])[0].data[ymin:ymax+1,xmin:xmax+1] 
  mom2_mod = fits.open(outfolder+'/maps/'+files_mod2[k])[0].data[ymin:ymax+1,xmin:xmax+1] 
  to_plot = [[mom0,mom1-vsys_m,mom2],[mom0_mod,mom1_mod-vsys_m,mom2_mod],[mom0-mom0_mod,mom1-mom1_mod,mom2-mom2_mod]] 

  nrows, ncols, x_len, y_len = 3, 3, 0.2, 0.2 
  fig, ax = defineaxis(nrows,ncols,x_len,y_len,xsep=0.00,ysep=0.08,fig_width=11,fig_heigth=11) 

  for i in range (ax.shape[0]): 
    cmap = copy(cmaps[i]) 
    cmap.set_bad('w',1.) 
    vmin, vmax = interval.get_limits(to_plot[1][i]) 
    vmin, vmax = (-1.1*np.nanmax(vmax),1.1*np.nanmax(vmax)) if i==1 else (vmin,vmax) 
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax) 
    cbax = fig.add_axes([ax[i][0].get_position().x0,ax[i][0].get_position().y0-0.025,2*x_len-0.003,0.02]) 
    cb1 = ColorbarBase(cbax, orientation='horizontal', cmap=cmap, norm=norm) 
    cb1.set_label(barlab[i],fontsize=13) 
    for j in range (ax.shape[1]): 
      axis = ax[i][j] 
      axis.tick_params(labelbottom=False,labelleft=False,right=True,top=True) 
      axis.set_xlim(ext[0],ext[1]) 
      axis.set_ylim(ext[2],ext[3]) 
      if j==2: 
        vmax = np.nanmax(interval.get_limits(to_plot[j][i])) 
        norm = mpl.colors.Normalize(vmin=-vmax, vmax=vmax) 
      pp = np.pad(to_plot[j][i]*maskmap,(pad_y, pad_x),mode='constant',constant_values=np.nan) 
      axis.imshow(pp,origin='lower',cmap=cmap,norm=norm,aspect='auto',extent=ext,interpolation='nearest') 
      axis.plot(xcen,ycen,'x',color='#000000',markersize=7,mew=1.5,zorder=10) 

      if i==0: 
        axis.text(0.5,1.05,titles[j],ha='center',transform=axis.transAxes,fontsize=15) 
        axis.plot(x,y,'--',color='k',linewidth=1) 
        if j!=2 and nr>3:  
          axmaj = rad_pix[-1] 
          axmin = axmaj*np.cos(np.radians(inc_m))  
          posa = np.radians(pa_m-90)  
          t = np.linspace(0,2*np.pi,100)  
          xt = xcen+axmaj*np.cos(posa)*np.cos(t)-axmin*np.sin(posa)*np.sin(t)  
          yt = ycen+axmaj*np.sin(posa)*np.cos(t)+axmin*np.cos(posa)*np.sin(t)  
          axis.plot(xt,yt,'-',c='k',lw=0.8)  
      elif i==1: 
        axis.plot(x,y,'--',color='k',linewidth=1) 
        if nr<10: 
          x_pix = rad_pix*np.cos(np.radians(pa_m-90)) 
          y_pix = rad_pix*np.sin(np.radians(pa_m-90)) 
          axis.scatter(x_pix+xcen,y_pix+ycen,c='grey',s=12) 
          axis.scatter(xcen-x_pix,ycen-y_pix,c='grey',s=12) 
        if nr>5 and not all(np.diff(pa)==0): 
          x_pix = rad_pix*np.cos(np.radians(pa-90)) 
          y_pix = rad_pix*np.sin(np.radians(pa-90)) 
          axis.plot(xcen-x_pix,ycen-y_pix,'-',color='grey',lw=1) 
          axis.plot(x_pix+xcen,y_pix+ycen,'-',color='grey',lw=1) 
        if j!=2: 
          cmax = np.nanmax(np.abs(to_plot[0][i])) 
          levels = np.linspace(0.166 * cmax, cmax, 6) 
          axis.contour(pp,levels=[0],colors='forestgreen',origin='lower',extent=ext) 
          axis.contour(pp,levels=-levels[::-1],colors='navy',linewidths=0.7,origin='lower',extent=ext,linestyles='solid') 
          axis.contour(pp,levels=levels,colors='darkred',linewidths=0.7,origin='lower',extent=ext) 
      if j==0: axis.text(-0.12,0.5,mapname[i],va='center',rotation=90,transform=axis.transAxes,fontsize=15) 

    cbax = fig.add_axes([ax[i][2].get_position().x0+0.003,ax[i][2].get_position().y0-0.025,x_len-0.003,0.02]) 
    cb2 = ColorbarBase(cbax, orientation='horizontal', cmap=cmap, norm=norm) 
    cb2.set_label(barlab2[i],fontsize=13) 
    cb2.ax.locator_params(nbins=3) 
    for c in [cb1,cb2]: 
      c.solids.set_edgecolor('face') 
      c.outline.set_linewidth(0) 

  outfile = '%s_maps'%outprefix 
  ntype   = files_mod0[k][files_mod0[k].rfind('_'):].replace('.fits','') 
  fig.savefig(outfolder+outfile+ntype+'.pdf', bbox_inches = 'tight') 

