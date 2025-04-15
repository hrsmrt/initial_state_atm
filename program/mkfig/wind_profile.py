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

filename = "wind_profile.jpeg"
data = np.loadtxt(data_path)
vgrid_c = np.loadtxt(f"{database_dir}vgrid/vgrid_c74.txt")

plt.plot(data,vgrid_c/1e3)
plt.xlabel("m/s")
plt.ylabel("km")
plt.grid(True)
save_path = "fig/" + filename
plt.savefig(save_path,
            dpi=200,
            bbox_inches="tight",
            pad_inches=0.05)
plt.close()