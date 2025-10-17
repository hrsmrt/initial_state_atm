import os
import sys
import numpy as np
import matplotlib.pyplot as plt
# Prefer params from current working dir ./setting/params.py; fall back to program/utils
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), 'setting')))
try:
	import params
except Exception:
	sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
	import params
settings = params.settings
database_dir = getattr(params, 'database_dir', '')

if len(sys.argv) > 1:
    mpl_style_sheet = sys.argv[1]

data_dir = f"{settings['filepath_params']['output_folderpath']}/data/"
output_dir = f"{settings['filepath_params']['output_folderpath']}/fig/cart/pre_yz/"
output_dir2 = f"{settings['filepath_params']['output_folderpath']}/fig/cart/pre_zx/"
output_dir3 = f"{settings['filepath_params']['output_folderpath']}/fig/cart/pre_xy/"
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
	data = np.fromfile(data_dir + settings["filepath_params"]["fname_pre"],dtype=np.float64) * 1e-2
	data = data.reshape(nz,ny,nx)
	print("min: ",np.min(data))
	print("max: ",np.max(data))
	Y,Z = np.meshgrid(ygrid, vgrid_c)
	for x in range(0,nx,int(nx/16)):
		plt.style.use(mpl_style_sheet)
		plt.xticks([0,int(max(ygrid))],[0,int(max(ygrid)/1e3)])
		plt.yticks([0,10e3,20e3,30e3,40e3],["0","10","20","30","40"])
		plt.xlabel("y (km)")
		plt.ylabel("z (km)")
		plt.contourf(Y,Z,data[:,:,x], levels=20, cmap="jet",extend="both")
		plt.colorbar(label="hPa")
		plt.savefig(output_dir + f"x{x:02d}.png")
		plt.close()
	X,Z = np.meshgrid(xgrid, vgrid_c)
	for y in range(0,ny,int(nx/16)):
		plt.style.use(mpl_style_sheet)
		plt.xticks([0,int(max(xgrid))],[0,int(max(xgrid)/1e3)])
		plt.yticks([0,10e3,20e3,30e3,40e3],["0","10","20","30","40"])
		plt.xlabel("x (km)")
		plt.ylabel("z (km)")
		plt.contourf(X,Z,data[:,y,:], levels=20, cmap="jet",extend="both")
		plt.colorbar(label="hPa")
		plt.savefig(output_dir2 + f"y{y:02d}.png")
		plt.close()
	X,Y = np.meshgrid(xgrid, ygrid)
	for z in range(0,nz,5):
		plt.style.use(mpl_style_sheet)
		plt.xlabel("x (km)")
		plt.ylabel("y (km)")
		plt.xticks([0,int(max(xgrid))],[0,int(max(xgrid)/1e3)])
		plt.yticks([0,int(max(ygrid))],[0,int(max(ygrid)/1e3)])
		plt.contourf(X,Y,data[z,:,:], levels=20, cmap="jet",extend="both")
		plt.colorbar(label="hPa")
		plt.savefig(output_dir3 + f"z{z:02d}.png")
		plt.close()
   
if __name__ == "__main__":
  main()
