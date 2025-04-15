import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
import numpy as np
import matplotlib.pyplot as plt
from params import settings
from params import database_dir

data_dir = settings["filepath_params"]["output_folderpath"] \
            + settings["vortex_param"]["vortex_folder"]
output_dir = "./fig/vortex/rz/"
os.makedirs(output_dir, exist_ok=True)

vortex_size = settings["vortex_param"]["vortex_size"]
nz = settings["setting_params"]["nz"]
nr = settings["vortex_param"]["nr"]
dr = vortex_size / nr

vgrid_c = np.loadtxt(f"{database_dir}vgrid/vgrid_c74.txt")
grid_r = np.array([i * dr for i in range(nr)])
bs_pre = np.loadtxt(f"{database_dir}sounding/sounding_gl9T28/bs_pres.dat")
bs_tem = np.loadtxt(f"{database_dir}sounding/sounding_gl9T28/bs_tem.dat")
bs_rho = np.loadtxt(data_dir + "bs_rho.txt")

X,Y = np.meshgrid(grid_r*1e-3, vgrid_c*1e-3)


def main():
	set_plt()
	data = np.loadtxt(data_dir + "vor_v.txt")
	data = data.reshape(nz,nr)
	plt.contourf(X,Y,data, levels=20, cmap="jet")
	save_fig("vor_v_all.jpeg")
	plt.ylim(0, 20)
	save_fig("vor_v.jpeg")
	plt.close()
	set_plt()
	data = np.loadtxt(data_dir + "vor_p.txt")
	data = data.reshape(nz,nr)
	for i in range(nz):
		data[i,:] = data[i,:] - bs_pre[i]
	plt.contourf(X,Y,data*1e-2, levels=20, cmap="jet_r")
	plt.colorbar()
	save_fig("vor_p_all.jpeg")
	plt.ylim(0, 20)
	save_fig("vor_p.jpeg")
	plt.close()
	set_plt()
	data = np.loadtxt(data_dir + "vor_T.txt")
	data = data.reshape(nz,nr)
	for i in range(nz):
		data[i,:] = data[i,:] - bs_tem[i]
	plt.contourf(X[:60,:],Y[:60,:],data[:60,:], levels=20, cmap="seismic",vmax=4, vmin=-4)
	plt.colorbar()
	save_fig("vor_T_all.jpeg")
	plt.ylim(0, 20)
	save_fig("vor_T.jpeg")
	plt.close()
	set_plt()
	data = np.loadtxt(data_dir + "vor_rho.txt")
	data = data.reshape(nz,nr)
	for i in range(nz):
		data[i,:] = data[i,:] - bs_rho[i]
	plt.contourf(X,Y,data, levels=20, cmap="seismic", vmax=0.018, vmin=-0.018)
	plt.colorbar()
	save_fig("vor_rho_all.jpeg")
	plt.ylim(0, 20)
	save_fig("vor_rho.jpeg")
	plt.close()


def set_plt():
	plt.figure(figsize=(4,4)) # inch
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
	plt.xlabel("r (km)")
	plt.ylabel("z (km)")
	plt.grid(True)
	# plt.axis('equal')

def save_fig(filename):
	plt.savefig(output_dir + filename,
				dpi=200,
				bbox_inches="tight",
				pad_inches=0.05)

if __name__ == "__main__":
		main()
