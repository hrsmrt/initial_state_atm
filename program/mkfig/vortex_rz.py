import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import numpy as np
import matplotlib.pyplot as plt
from params import settings

data_dir = settings["filepath_params"]["output_folderpath"] \
            + settings["vortex_param"]["vortex_folder"]
output_dir = "./fig/vortex/rz/"
os.makedirs(output_dir, exist_ok=True)

vortex_size = settings["vortex_param"]["vortex_size"]
nz = settings["setting_params"]["nz"]
nr = settings["vortex_param"]["nr"]
dr = vortex_size / nr

vgrid_c = np.loadtxt(settings["filepath_params"]["filepath_vgrid_c"])
grid_r = np.array([i * dr for i in range(nr)])
bs_pre = np.loadtxt(settings["filepath_params"]["filepath_bs_pre"])
bs_tem = np.loadtxt(settings["filepath_params"]["filepath_bs_tem"])
bs_rho = np.loadtxt(data_dir + "bs_rho.txt")

plt_style = settings["mkfig_params"]["plt_style"]

X,Y = np.meshgrid(grid_r*1e-3, vgrid_c*1e-3)

def main():
	set_plt()
	fig, ax = plt.subplots(figsize=(2.5,2)) # inch
	data = np.loadtxt(data_dir + "vor_v.txt")
	data = data.reshape(nz,nr)
	c = ax.contourf(X,Y,data, levels=20, cmap="jet")
	fig.colorbar(c)
	ax.set_xticks([0,1000])
	ax.minorticks_on()
	ax.grid(which='major', axis='both', color='gray', linewidth=0.8)
	ax.grid(which='minor', axis='both', color='gray', linestyle=':', linewidth=0.5)
	ax.set_ylim(0, 40)
	ax.set_yticks([0,40])
	plt.savefig(f"{output_dir}vor_v_all.png")
	ax.set_ylim(0, 20)
	ax.set_yticks([0,20])
	plt.savefig(f"{output_dir}vor_v.png")
	plt.close()

	set_plt()
	fig, ax = plt.subplots(figsize=(2.5,2)) # inch
	ax.set_title("気圧偏差 [hPa]")
	data = np.loadtxt(data_dir + "vor_p.txt")
	data = data.reshape(nz,nr)
	for i in range(nz):
		data[i,:] = data[i,:] - bs_pre[i]
	c = ax.contourf(X,Y,data*1e-2, levels=20, cmap="jet_r")
	fig.colorbar(c)
	ax.set_xticks([0,1000])
	ax.minorticks_on()
	ax.grid(which='major', axis='both', color='gray', linewidth=0.8)
	ax.grid(which='minor', axis='both', color='gray', linestyle=':', linewidth=0.5)
	ax.set_ylim(0, 40)
	ax.set_yticks([0,40])
	plt.savefig(f"{output_dir}vor_p_all.png")
	ax.set_ylim(0, 20)
	ax.set_yticks([0,20])
	plt.savefig(f"{output_dir}vor_p.png")
	plt.close()

	set_plt()
	fig, ax = plt.subplots(figsize=(2.5,2)) # inch
	data = np.loadtxt(data_dir + "vor_T.txt")
	data = data.reshape(nz,nr)
	for i in range(nz):
		data[i,:] = data[i,:] - bs_tem[i]
	c = ax.contourf(X[:70,:],Y[:70,:],data[:70,:], levels=20, cmap="seismic",vmax=4, vmin=-4)
	fig.colorbar(c)
	ax.set_title("気温偏差 [K]")
	ax.set_xticks([0,1000])
	ax.set_ylim(0,40)
	ax.set_yticks([0,40])
	ax.minorticks_on()
	ax.grid(which='major', axis='both', color='gray', linewidth=0.8)
	ax.grid(which='minor', axis='both', color='gray', linestyle=':', linewidth=0.5)
	plt.savefig(f"{output_dir}vor_T_all.png")
	plt.close()
	
	set_plt()
	fig, ax = plt.subplots(figsize=(2.5,2)) # inch
	c = ax.contourf(X[:60,:],Y[:60,:],data[:60,:], levels=20, cmap="seismic",vmax=4, vmin=-4)
	fig.colorbar(c)
	ax.set_title("気温偏差 [K]")
	ax.set_xticks([0,1000])
	ax.set_ylim(0,20)
	ax.set_yticks([0,20])
	ax.minorticks_on()
	ax.grid(which='major', axis='both', color='gray', linewidth=0.8)
	ax.grid(which='minor', axis='both', color='gray', linestyle=':', linewidth=0.5)
	plt.savefig(f"{output_dir}vor_T.png")
	plt.close()

	set_plt()
	fig, ax = plt.subplots(figsize=(2.5,2)) # inch
	data = np.loadtxt(data_dir + "vor_rho.txt")
	data = data.reshape(nz,nr)
	for i in range(nz):
		data[i,:] = data[i,:] - bs_rho[i]
	c = ax.contourf(X,Y,data*1e2, levels=20, cmap="seismic", vmax=1.8, vmin=-1.8)
	fig.colorbar(c)
	ax.set_title(r"密度偏差 [$ \times 10^{-2}$ kg/m$^3$]")
	ax.set_xticks([0,1000])
	ax.minorticks_on()
	ax.grid(which='major', axis='both', color='gray', linewidth=0.8)
	ax.grid(which='minor', axis='both', color='gray', linestyle=':', linewidth=0.5)
	ax.set_ylim(0, 40)
	ax.set_yticks([0,40])
	plt.savefig(f"{output_dir}vor_rho_all.png")
	ax.set_ylim(0, 20)
	ax.set_yticks([0,20])
	plt.savefig(f"{output_dir}vor_rho.png")
	plt.close()

def set_plt():
	plt.figure(figsize=(2.5,2)) # inch
	plt.style.use(plt_style)
	plt.xlabel("半径 [km]")
	plt.ylabel("高度 [km]")

if __name__ == "__main__":
		main()
