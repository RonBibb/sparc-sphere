###############################################################
#### This script contains some utilities for plotting      ####
###############################################################
import numpy as np 
import matplotlib.pyplot as plt 

def defineaxis(nrows,ncols,xlen,ylen,xsep=0,ysep=0,fig_width=8.27,fig_heigth=11.69, fig=None):

  if not fig: fig = plt.figure(figsize=(fig_width, fig_heigth)) 
  fig_width, fig_heigth = fig.get_size_inches() 
  fig_ratio = fig_width / fig_heigth 

  ax = [] 
  for i in range(nrows):
    row = []
    y = -(i * (ylen + ysep) * fig_ratio)
    for j in range(ncols):
      x = j * (xlen + xsep)
      row.append(fig.add_axes([x, y, xlen, ylen * fig_ratio])) 
    ax.append(row)
  return fig, np.squeeze(ax)

def calculate_padding(xsize,ysize):
  n = max(ysize, xsize) 
  pad_y = ((n - ysize) // 2, n - ysize - (n - ysize) // 2) 
  pad_x = ((n - xsize) // 2, n - xsize - (n - xsize) // 2) 
  return (pad_x,pad_y)

def build_path(x0, y0, rad_pix, pa_deg, nx, ny, oversampling=1):

  from scipy.interpolate import make_splprep
  # 1. Ring points 
  pa_to_xy = lambda r, pa: (x0-r*np.sin(pa), y0+r*np.cos(pa))

  xy_pos = [pa_to_xy(r, np.radians(pa)) for r, pa in zip(rad_pix, pa_deg)]
  xy_neg = [pa_to_xy(-r, np.radians(pa)) for r, pa in zip(rad_pix[::-1], pa_deg[::-1])]
  xy_ring = np.concatenate([xy_neg,[[x0,y0]],xy_pos])

  # 2. Spline fit
  spl, u = make_splprep(xy_ring.T, s=0)
  u_inner = np.linspace(0, 1, xy_ring.shape[0]*3)
  x_s, y_s = spl(u_inner)

  # 3. Tangents at ends
  t0 = spl(0.0, nu=1)
  t1 = spl(1.0, nu=1)
  t0 /= np.hypot(*t0)
  t1 /= np.hypot(*t1)

  # 4. Extend linearly
  n_ext = int(np.maximum(nx,ny)/2)
  s_ext = np.linspace(1, n_ext + 1, n_ext*oversampling)
  xf = x_s[-1] + s_ext * t1[0]
  yf = y_s[-1] + s_ext * t1[1]
  xb = x_s[0] - s_ext * t0[0]
  yb = y_s[0] - s_ext * t0[1]

  # 5. Combine full slit and select points within field
  x = np.concatenate([xb[::-1], x_s, xf])
  y = np.concatenate([yb[::-1], y_s, yf])
  mask = (x >= 0) & (x <= nx - 1) & (y >= 0) & (y <= ny - 1)
  x, y = x[mask], y[mask]

  # 6. Calculating distances along the path
  icenter = np.argmin((x - x0)**2 + (y - y0)**2)
  ds = np.hypot(np.diff(x), np.diff(y))
  s = np.concatenate([[0.0], np.cumsum(ds)])

  # 7. Sorting and interpolating across a uniform grid
  idx = np.argsort(s)
  x, y, s = x[idx], y[idx], s[idx]-s[icenter]
  sp = np.arange(s.min(),s.max(),1/oversampling)
  xp, yp = np.interp(sp,s,x), np.interp(sp,s,y)

  return sp,xp,yp

def extract_pv(array, x, y, order=1, width=1, oversampling=1):

  from scipy.ndimage import map_coordinates 
  zsize, ysize, xsize = array.shape[:3] 
  zs = np.outer(np.arange(0, zsize, 1.0/oversampling), np.ones(len(x)))
  z_len = zs.shape[0]

  dx = np.gradient(x)
  dy = np.gradient(y)
  norm = np.hypot(dx, dy)
  nx, ny = dy / norm, -dx / norm

  nwidth = 2*width + 1
  offsets = np.linspace(-width/2.0, width/2.0, nwidth)

  has_nan = np.any(np.isnan(array))
  samples = []
  for off in offsets:
    xs = x + off * nx
    ys = y + off * ny
    xs_grid = np.outer(np.ones(z_len), xs)
    ys_grid = np.outer(np.ones(z_len), ys)

    if has_nan:
      vals = map_coordinates(np.nan_to_num(array),[zs,ys_grid,xs_grid],order=int(order),cval=np.nan)
      bad  = map_coordinates(np.isnan(array).astype(float),[zs,ys_grid,xs_grid],order=0,cval=1.0) > 0
      vals[bad] = np.nan
    else:
      vals = map_coordinates(array,[zs,ys_grid,xs_grid],order=int(order),cval=np.nan)

    samples.append(vals)
  return np.nanmean(np.stack(samples, axis=0), axis=0)
