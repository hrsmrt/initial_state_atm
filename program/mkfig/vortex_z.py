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

plt.figure(figsize=(8,8)) # inch
#plt.rcParams['font.family'] ='Hiragino Maru Gothic Pro'
# plt.rcParams['text.usetex'] = True # 日本語と併用不可
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['font.size'] = 12 # pt
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['xtick.major.width'] = 0.55
plt.rcParams['ytick.major.width'] = 0.55
# plt.xlim(300,400)
# plt.xscale('log')
# plt.yscale('log')
# plt.scatter(pix, count, label='', s=5)
plt.xlabel("m/s")
plt.ylabel("km")
plt.grid(True)
# plt.axis('equal')

data = np.loadtxt(data_dir + "v_z.txt")
plt.plot(data,vgrid_c*1e-3)
plt.savefig(output_dir + "v_z.png",
			dpi=200,
			bbox_inches="tight",
			pad_inches=0.05)
plt.close()
