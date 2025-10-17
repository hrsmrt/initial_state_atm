"""
Python version of mkdata/cartesian.f90

This script reproduces the behavior of the Fortran program in a numpy-based
implementation: reading base-state profiles, optional vortex addition,
optional u-profile addition, and writing 1D text and 3D binary outputs.

It expects the project's `program/utils/params.py` to exist and to provide the
`settings` dictionary used to configure paths and parameters.
"""
import os
import sys
import numpy as np

# Prefer params from current working dir ./setting/params.py; fall back to program/utils
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), 'setting')))
try:
	import params
except Exception:
	sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))
	import params

def main():
    settings = params.settings

    # setting params
    s = settings['setting_params']
    triangle_size = s['triangle_size']
    nx = int(s['nx'])
    ny = int(s['ny'])
    nz = int(s['nz'])
    add_vortex_flg = bool(s.get('add_vortex_flg', False))
    add_u_profile_flg = bool(s.get('add_u_profile_flg', False))
    add_perturbation_tem_flg = bool(s.get('add_perturbation_tem_flg', False))
    perturbation_tem_top = settings['perturbation_param']['perturbation_tem_top']

    vgrid = np.loadtxt(settings["filepath_params"]["filepath_vgrid_c"], dtype=np.float64)

    # vortex params
    v = settings.get('vortex_param', {})
    vortex_size = v.get('vortex_size')
    nr = int(v.get('nr'))

    # filepaths
    fp = settings['filepath_params']
    output_folderpath = os.path.join(fp['output_folderpath'], 'data/')
    os.makedirs(output_folderpath, exist_ok=True)

    # cart params (vor_cx, vor_cy provided as integers in settings)
    cartp = settings.get('cart_param', {})
    vor_cx = int(cartp.get('vor_cx', 0))
    vor_cy = int(cartp.get('vor_cy', 0))

    # allocate arrays (use Fortran order so tofile in Fortran-order later)
    bs_pre = np.zeros(nz, dtype=np.float64)
    bs_tem = np.zeros(nz, dtype=np.float64)
    bs_qv = np.zeros(nz, dtype=np.float64)
    u_profile = np.zeros(nz, dtype=np.float64)

    vor_p = np.zeros((nr, nz), dtype=np.float64)
    vor_T = np.zeros((nr, nz), dtype=np.float64)
    vor_v = np.zeros((nr, nz), dtype=np.float64)
    vor_rho = np.zeros((nr, nz), dtype=np.float64)

    pre = np.zeros((nx, ny, nz), dtype=np.float64, order='F')
    tem = np.zeros((nx, ny, nz), dtype=np.float64, order='F')
    rho = np.zeros((nx, ny, nz), dtype=np.float64, order='F')
    qv = np.zeros((nx, ny, nz), dtype=np.float64, order='F')
    u = np.zeros((nx, ny, nz), dtype=np.float64, order='F')
    v_arr = np.zeros((nx, ny, nz), dtype=np.float64, order='F')

    # helper IO functions
    def input_bsdata(target, input_file):
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"Failed to open file '{input_file}' for input")
        data = np.loadtxt(input_file, dtype=np.float64)
        if data.size != target.size:
            # try to accept if file is single column or row
            if data.ndim == 1 and data.size == target.size:
                target[:] = data
            else:
                raise ValueError(f"Input size mismatch for {input_file}: expected {target.size}, got {data.size}")
        else:
            target[:] = data

    def input_data_vortex(target, filename):
        # default vortex data folder
        filepath = os.path.join('data', 'vortex', filename)
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Failed to open file '{filepath}' for input")
        data = np.loadtxt(filepath, dtype=np.float64)
        # allow both (nr, nz) shaped files or flat files
        if data.ndim == 1:
            if data.size != nr * nz:
                raise ValueError(f"Vortex file {filepath} size mismatch: expected {nr*nz}, got {data.size}")
            target[:, :] = data.reshape((nr, nz))
        else:
            # if loader returns 2D, try to fit
            arr = np.array(data)
            if arr.shape != (nr, nz):
                # try transpose
                if arr.shape == (nz, nr):
                    target[:, :] = arr.T
                else:
                    raise ValueError(f"Vortex file {filepath} shape mismatch: expected {(nr,nz)}, got {arr.shape}")
            else:
                target[:, :] = arr

    def output_1d(data, filename):
        filepath = os.path.join(output_folderpath, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        np.savetxt(filepath, data)

    def output_3d(data, filename):
        filepath = os.path.join(output_folderpath, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # reorder axes to (z, y, x) before writing so the file contains
        # data in (z,y,x) layout. We write in Fortran (column-major) order
        # of the transposed array to keep a deterministic memory layout.
        arr = np.transpose(data, (2, 1, 0))
        with open(filepath, 'wb') as f:
            np.asfortranarray(arr).tofile(f)

    # read base-state and profiles
    input_bsdata(bs_pre, fp['filepath_bs_pre'])
    input_bsdata(bs_tem, fp['filepath_bs_tem'])
    input_bsdata(bs_qv, fp['filepath_bs_qv'])
    # only read u_profile if the flag requests adding a u-profile
    if add_u_profile_flg:
        input_bsdata(u_profile, fp['filepath_u_profile'])

    # fill 3D fields with base-state
    for k in range(nz):
        pre[:, :, k] = bs_pre[k]
        tem[:, :, k] = bs_tem[k]
        qv[:, :, k] = bs_qv[k]

    # optional: read vortex data (only if adding vortex later may require it)
    try:
        input_data_vortex(vor_p, 'vor_p.txt')
    except FileNotFoundError:
        pass
    try:
        input_data_vortex(vor_T, 'vor_T.txt')
    except FileNotFoundError:
        # some runs may not have T vortex; allow zeros
        pass
    try:
        input_data_vortex(vor_v, 'vor_v.txt')
    except FileNotFoundError:
        pass

    # add vortex
    if add_vortex_flg:
        add_vortex(pre, tem, rho, u, v_arr, vor_p, vor_T, vor_v, vor_rho,
                   vor_cx, vor_cy, triangle_size, nx, ny, nz, vortex_size, nr)

    # add u profile
    if add_u_profile_flg:
        for k in range(nz):
            u[:, :, k] = u[:, :, k] + u_profile[k]

    # add perturbation to temperature
    if add_perturbation_tem_flg:
        for k in range(nz):
            if vgrid[k] > perturbation_tem_top:
                break
            tem[:, :, k] = tem[:, :, k] + np.random.normal(0, 0.1, size=tem[:, :, k].shape)


    # output
    output_1d(bs_pre, fp['fname_bs_pre'])
    output_1d(bs_tem, fp['fname_bs_tem'])
    output_1d(bs_qv, fp['fname_bs_qv'])
    output_3d(pre, fp['fname_pre'])
    output_3d(tem, fp['fname_tem'])
    output_3d(qv, fp['fname_qv'])
    output_3d(u, fp['fname_u'])
    output_3d(v_arr, fp['fname_v'])


def add_vortex(pre, tem, rho, u, v_arr, vor_p, vor_T, vor_v, vor_rho,
               vor_cx, vor_cy, triangle_size, nx, ny, nz, vortex_size, nr):
    # follow Fortran logic; loops are 1-based in Fortran, so emulate that
    dx = triangle_size / float(nx)
    dy = triangle_size / float(ny)
    dr = vortex_size / float(nr)

    logpath = os.path.join('log', 'cartesian.txt')
    os.makedirs(os.path.dirname(logpath), exist_ok=True)
    with open(logpath, 'w') as logfile:
        for k in range(1, nz + 1):
            k_idx = k - 1
            for j in range(1, ny + 1):
                j_idx = j - 1
                for i in range(1, nx + 1):
                    i_idx = i - 1
                    dist_x = float(i - vor_cx) * dx
                    dist_y = float(j - vor_cy) * dy
                    dist = np.hypot(dist_x, dist_y)
                    if dist == 0.0:
                        sin_theta = 0.0
                        cos_theta = 0.0
                    else:
                        sin_theta = dist_y / dist
                        cos_theta = dist_x / dist

                    if dist < vortex_size:
                        dist_index = dist / dr
                        dist_index_int = int(dist_index)
                        ratio1 = dist_index - float(dist_index_int)
                        ratio2 = 1.0 - ratio1
                        if k == 1 and (j % 20 == 0) and (i % 20 == 0):
                            logfile.write(f"i = {i} j = {j} k = {k}\n")
                            logfile.write(f"vor_cx = {vor_cx}\n")
                            logfile.write(f"vor_cy = {vor_cy}\n")
                            logfile.write(f"dist_x = {dist_x}\n")
                            logfile.write(f"dist_y = {dist_y}\n")
                            logfile.write(f"dist = {dist}\n")
                            logfile.write(f"vortex_size = {vortex_size}\n")
                            logfile.write(f"dist_index = {dist_index}\n")
                            logfile.write(f"dist_index_int = {dist_index_int}\n")
                            logfile.write(f"ratio1 = {ratio1}\n")
                            logfile.write(f"ratio2 = {ratio2}\n")

                        if dist_index_int < nr - 1:
                            di = dist_index_int
                            # di and di+1 are 0-based indices for vor_* arrays
                            pre[i_idx, j_idx, k_idx] = (
                                ratio2 * vor_p[di, k_idx] + ratio1 * vor_p[di + 1, k_idx]
                            )
                            tem[i_idx, j_idx, k_idx] = (
                                ratio2 * vor_T[di, k_idx] + ratio1 * vor_T[di + 1, k_idx]
                            )
                            rho[i_idx, j_idx, k_idx] = (
                                ratio2 * vor_rho[di, k_idx] + ratio1 * vor_rho[di + 1, k_idx]
                            )
                            vv = (ratio2 * vor_v[di, k_idx] + ratio1 * vor_v[di + 1, k_idx])
                            u[i_idx, j_idx, k_idx] = - vv * sin_theta
                            v_arr[i_idx, j_idx, k_idx] = vv * cos_theta


if __name__ == '__main__':
    main()
# 設定を元に、直交座標のデータを出力
# 出力データの形式は、NICAMの入力データ形式に準拠