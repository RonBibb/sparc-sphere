########################################################################
#### This script simply calls all other python scripts for plotting ####
########################################################################
import os 

scriptdir = 'out_NGC_2841/plotscripts/' 
cmd = '' 

for f in os.listdir(scriptdir): 
  if '.py' in f and f!='plot_all.py' and f!='plot_utils.py': 
    cmd += 'python "%s/%s" & '%(scriptdir,f) 

os.system(cmd[:-2]) 
