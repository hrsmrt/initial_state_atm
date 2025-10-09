import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import numpy as np
import matplotlib.pyplot as plt
from params import settings
from params import database_dir

data_path = settings["filepath_params"]["output_folderpath"] \
            + settings["wind_profile_param"]["wind_profile_folder"] \
            + settings["wind_profile_param"]["filename"]

plt_style = settings["mkfig_params"]["plt_style"]

output_filename = "wind_profile.png"
data = np.loadtxt(data_path)
vgrid_c = np.loadtxt(f"{database_dir}vgrid/vgrid_c74.txt")

plt.style.use(plt_style)
fig, ax = plt.subplots(figsize=(3,4))
ax.plot(data,vgrid_c/1e3)
ax.set_xlabel("m/s")
ax.set_ylabel("km")
ax.grid(True)
plt.savefig(f"fig/{output_filename}")
plt.close()
