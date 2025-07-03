import os
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
from params import settings
from params import database_dir

data_dir = "./data/cart/"
output_dir = "./fig/cart/qv_yz/"
output_dir2 = "./fig/cart/qv_zx/"
output_dir3 = "./fig/cart/qv_xy/"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(output_dir2, exist_ok=True)
os.makedirs(output_dir3, exist_ok=True)
vgrid_c = np.loadtxt(f"{database_dir}vgrid/vgrid_c74.txt")

nx = settings["setting_params"]["nx"]
ny = settings["setting_params"]["ny"]
nz = settings["setting_params"]["nz"]
triangle_size = settings["setting_params"]["triangle_size"]
dx = triangle_size / nx
dy = triangle_size / ny
nyz = ny * nz

xgrid = np.array([dx * 0.5 + i * dx for i in range(nx)])
ygrid = np.array([dy * 0.5 + i * dy for i in range(ny)])


def main():
	set_plt()
	data = np.fromfile(data_dir + settings["filepath_params"]["fname_qv"],dtype=np.float64)
	data = data.reshape(nx,ny,nz)
	print("min: ",np.min(data))
	print("max: ",np.max(data))
	X,Y = np.meshgrid(ygrid * 1e-3, vgrid_c * 1e-3)
	for x in range(0,nx,int(nx/16)):
		set_plt()
		plt.xticks([16,2048,4080],[0,2048,4096])
		plt.yticks([10,20,30])
		plt.xlabel("y (km)")
		plt.ylabel("z (km)")
		plt.contourf(X,Y,data[x,:,:].T, levels=20, cmap="jet",extend="both")
		plt.colorbar(label="kg/kg")
		save_fig(output_dir,f"x{x:02d}.jpeg")
		plt.close()
	X,Y = np.meshgrid(xgrid * 1e-3, vgrid_c * 1e-3)
	for y in range(0,ny,int(nx/16)):
		set_plt()
		plt.xticks([16,2048,4080],[0,2048,4096])
		plt.yticks([10,20,30])
		plt.xlabel("x (km)")
		plt.ylabel("z (km)")
		plt.contourf(X,Y,data[:,y,:].T, levels=20, cmap="jet",extend="both")
		plt.colorbar(label="kg/kg")
		save_fig(output_dir2,f"y{y:02d}.jpeg")
		plt.close()
	X,Y = np.meshgrid(xgrid * 1e-3, ygrid * 1e-3)
	for z in range(0,nz,5):
		set_plt()
		plt.xlabel("x (km)")
		plt.ylabel("y (km)")
		plt.xticks([16,2048,4080],[0,2048,4096])
		plt.xticks([16,2048,4080],[0,2048,4096])
		plt.contourf(X,Y,data[:,:,z].T, levels=20, cmap="jet",extend="both")
		plt.colorbar(label="kg/kg")
		save_fig(output_dir3,f"z{z:02d}.jpeg")
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
	plt.grid(True)
	# plt.axis('equal')
     
def save_fig(output_dir,filename):
	plt.savefig(output_dir + filename,
				dpi=200,
				bbox_inches="tight",
				pad_inches=0.05)

if __name__ == "__main__":
  main()
