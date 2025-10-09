triangle_size = 4096e3 # m
gl = 9
nx = 2 ** gl
ny = 2 ** gl
nz = 74
vortex_size = 1000e3 # m
dx = triangle_size / nx
dy = triangle_size / ny
nr_vor = 250
vor_cx_float = triangle_size * 0.25
vor_cx = int(vor_cx_float / dx)
vor_cy_float = triangle_size * 0.25 * 3 ** 0.5
vor_cy = int(vor_cy_float / dy)
database_dir = "hogehoge/database/"

settings = {
  "setting_params" : {
    "triangle_size" : triangle_size,
    "nx" : nx,
    "ny" : ny,
    "nz" : nz,
    "f"  : 3.774676e-05,
    "add_vortex_flg" : False,
    "add_u_profile_flg" : False,
  },
  "vortex_param" : {
    "vortex_folder" : "vortex/",
    "vortex_size" : vortex_size, # m
    "nr" : nr_vor,
    "a" : 0.3,
    "vmax" : 20.0, # m/s,
    "rmax" : 100000.0, # m,
    "rcut" : 700000.0, # m,
    "n_smooth" : 20,
    "zmax" : 2000,
    "lz_low" : 3175,
    "lz_high" : 4762.5,
    "beta" : 2.0,
    "n_balance" : 15,
    "z_calc_max" : 53
  },
  "wind_profile_param" : {
    "wind_profile_folder" : "wind_profile/",
    "filename" : "bs_u.txt",
    "filename_cnf" : "bs_u_cnf.txt",
    "shear_type" : "linear", # linear or sine
    "z1" : 2000,
    "z2" : 10000,
    "z3" : 50000,
    "z4" : 50000,
    "u1" : 0,
    "u2" : 5
  },
  "filepath_params" : {
    "filepath_vgrid_c" : f"{database_dir}vgrid/vgrid_c74.txt",
    "filepath_bs_pre" : f"{database_dir}sounding/sounding_gl9T28/bs_pres.dat",
    "filepath_bs_tem" : f"{database_dir}sounding/sounding_gl9T28/bs_tem.dat",
    "filepath_bs_qv" : f"{database_dir}sounding/sounding_gl9T28/bs_qv.dat",
    "filepath_u_profile" : "./data/wind_profile/bs_u.txt",
    "output_folderpath" : "./data/",
    "fname_bs_pre" : "bs_pre.txt",
    "fname_bs_tem" : "bs_tem.txt",
    "fname_bs_qv" : "bs_qv.txt",
    "fname_pre" : "pre.dat",
    "fname_tem" : "tem.dat",
    "fname_rho" : "rho.dat",
    "fname_qv" : "qv.dat",
    "fname_u" : "u.dat",
    "fname_v" : "v.dat",
  },
  "cart_param" : {
    "vor_cx" : vor_cx,
    "vor_cy" : vor_cy,
  }
}
