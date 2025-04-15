import numpy as np
import matplotlib.pyplot as plt
from params import database_dir

filename = "wind_profiles.jpeg"
vgrid_c = np.loadtxt(f"{database_dir}vgrid/vgrid_c74.txt")

dirs = ["z_shear_1", "z_shear_5", "z_shear_10", "z_shear_15", "z_shear_inf"]
labels = ["z_sh1","z_sh5", "z_sh10", "z_sh15", "z_sh_inf"]
for i in range(len(dirs)):
    label = labels[i]
    dir = dirs[i]
    file_path = dir + "/data.txt"
    data = np.loadtxt(file_path)
    plt.plot(data,vgrid_c/1e3, label=labels[i])
plt.xlim([-10,10])
plt.ylim([0,20])
plt.xlabel("m/s")
plt.ylabel("km")
plt.grid(True)
plt.legend()
plt.savefig(filename,
            dpi=200,
            bbox_inches="tight",
            pad_inches=0.05)
plt.close()
