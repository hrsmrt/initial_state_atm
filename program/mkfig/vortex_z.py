import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import numpy as np
import matplotlib.pyplot as plt
from params import settings
from params import database_dir

data_dir = settings["filepath_params"]["output_folderpath"] \
            + settings["vortex_param"]["vortex_folder"]
output_dir = "./fig/vortex/z/"
os.makedirs(output_dir, exist_ok=True)

vgrid_c = np.loadtxt(settings["filepath_params"]["filepath_vgrid_c"])

plt_style = settings["mkfig_params"]["plt_style"]

data = np.loadtxt(data_dir + "v_z.txt")

plt.style.use(plt_style)
fig, ax = plt.subplots(figsize=(2.5,2.5))
plt.plot(data,vgrid_c*1e-3)
plt.xticks([0,0.5,1])
plt.yticks([0,10,20,30,40])
plt.ylabel("高度 [km]")
plt.savefig(f"{output_dir}v_z.png")
plt.close()
