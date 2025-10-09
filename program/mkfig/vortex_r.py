import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import numpy as np
import matplotlib.pyplot as plt
from params import settings
from params import database_dir
from params import vortex_size, nr_vor

plt_style = settings["mkfig_params"]["plt_style"]

data_dir = settings["filepath_params"]["output_folderpath"] \
            + settings["vortex_param"]["vortex_folder"]
output_dir = "./fig/vortex/r/"
os.makedirs(output_dir, exist_ok=True)

dr = vortex_size / nr_vor
grid_r = np.array([i * dr for i in range(nr_vor)])

data = np.loadtxt(data_dir + "vt.txt")
plt.style.use(plt_style)
fig, ax = plt.subplots(figsize=(2.5,2))
ax.minorticks_on()
ax.plot(grid_r, data)
ax.set_ylim(0,22)
ax.set_xticks([0,10e5], labels=[0,1000])
ax.set_yticks([0,20])
ax.grid(which='major', axis='both', color='gray', linewidth=0.8)
ax.grid(which='minor', axis='both', color='gray', linestyle=':', linewidth=0.5)
ax.set_xlabel("半径 [km]")
ax.set_ylabel("風速 [m/s]")
plt.savefig(f"{output_dir}vt.png")
plt.close()

plt.style.use(plt_style)
fig, ax = plt.subplots(figsize=(2.5,2))
ax.minorticks_on()
data = np.loadtxt(data_dir + "v_r.txt")
ax.plot(grid_r, data)
ax.set_ylim(0,22)
ax.set_xticks([0,10e5], labels=[0,1000])
ax.set_yticks([0,20])
ax.grid(which='major', axis='both', color='gray', linewidth=0.8)
ax.grid(which='minor', axis='both', color='gray', linestyle=':', linewidth=0.5)
ax.set_xlabel("半径 [km]")
ax.set_ylabel("風速 [m/s]")
plt.savefig(f"{output_dir}v_r.png")
plt.close()

plt.style.use(plt_style)
fig, ax = plt.subplots(figsize=(2.5,2))
ax.minorticks_on()
data = np.loadtxt(data_dir + "v_smooth.txt")
ax.plot(grid_r, data)
ax.set_ylim(0,22)
ax.set_xticks([0,10e5], labels=[0,1000])
ax.set_yticks([0,20])
ax.grid(which='major', axis='both', color='gray', linewidth=0.8)
ax.grid(which='minor', axis='both', color='gray', linestyle=':', linewidth=0.5)
ax.set_xlabel("半径 [km]")
ax.set_ylabel("風速 [m/s]")
plt.savefig(f"{output_dir}v_smooth.png")
plt.close()

plt.style.use(plt_style)
fig, ax = plt.subplots(figsize=(5,3))
data = np.loadtxt(data_dir + "vt.txt")
ax.plot(grid_r, data, label="vt")
data = np.loadtxt(data_dir + "v_r.txt")
ax.plot(grid_r, data, label="v_r")
data = np.loadtxt(data_dir + "v_smooth.txt")
ax.plot(grid_r, data, label="v_smooth")
ax.set_ylim(0,22)
ax.set_xticks([0,10e5], labels=[0,1000])
ax.set_yticks([0,20])
ax.legend(fontsize=12)
ax.minorticks_on()
ax.grid(which='major', axis='both', color='gray', linewidth=0.8)
ax.grid(which='minor', axis='both', color='gray', linestyle=':', linewidth=0.5)
ax.set_xlabel("半径 [km]")
ax.set_ylabel("風速 [m/s]")
plt.savefig(f"{output_dir}v_all.png")
plt.close()
