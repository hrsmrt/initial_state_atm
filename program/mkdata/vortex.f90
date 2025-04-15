program vortex
  use filepaths
  use settings
  use constants
  use mod_vortex
  implicit none
  integer :: i,k
  
  vortex_size = 1000d3 ! m
  nr = 250
  nz = 74
  dr = vortex_size / real(nr)
  a = 0.3
  vmax = 20.0 ! m/s
  rmax = 100000.0 ! m
  rcut = 700000.0 ! m
  n_smooth = 20
  zmax = 2000.0 ! m
  lz_low = 3175 ! m
  lz_high = 4762.5 ! m
  lz = lz_low ! m
  beta = 2.0
  n_balance = 100
  filepath_vgrid_c = "./vgrid_c.txt"
  fpath_bs_pre = "./bs_p.txt"
  fpath_bs_tem = "./bs_T.txt"
  output_folderpath = "./"
  open(unit=10, file="config/param.nml")
  read(10, nml=setting_params)
  read(10, nml=vortex_param)
  read(10, nml=filepath_params)
  close(10)
  allocate(r(nr))
  allocate(v_r(nr))
  allocate(z(nz))
  allocate(v_z(nz))
  allocate(p_bs(nz))
  allocate(T_bs(nz))
  allocate(vor_v(nr,nz))
  allocate(vor_p(nr,nz))
  allocate(p_(nr,nz))
  allocate(vor_T(nr,nz))
  allocate(vor_rho(nr,nz))
  output_folderpath = trim(output_folderpath)//trim(vortex_folder)
  call execute_command_line("mkdir -p "//trim(output_folderpath))
  open(unit=11, file="log/vortex.txt", status='replace')
  write(11,*) "f = ", f
  write(11,*) "nr = ", nr
  write(11,*) "nz = ", nz
  write(11,*) "dr = ", dr
  write(11,*) "a = ", a
  write(11,*) "vmax = ", vmax
  write(11,*) "rmax = ", rmax
  write(11,*) "rcut = ", rcut
  write(11,*) "n_smooth = ", n_smooth
  write(11,*) "zmax = ", zmax
  write(11,*) "lz_low = ", lz_low
  write(11,*) "lz_high = ", lz_high
  write(11,*) "lz = ", lz
  write(11,*) "beta = ", beta
  write(11,*) "filepath_vgrid_c = ", filepath_vgrid_c
  write(11,*) "output_folderpath = ", output_folderpath
  call input_1d(z,filepath_vgrid_c)
  call input_1d(p_bs,fpath_bs_pre)
  call input_1d(T_bs,fpath_bs_tem)
  write(11,*) "z_index, z(高度), p(圧力), T(温度)"
  do i = nz, 1, -1
    write(11,*) "z(", i, ") = ", z(i), p_bs(i), T_bs(i)
  end do

  ! v(方位角方向風速)の半径方向分布
  do i = 1, nr
    r(i) = (i - 1) * dr
    v_r(i) = 0.d0
  end do
  do i = 1, nr
    if (r(i) < rmax) then
      v_r(i) = vmax * (r(i) / rmax)
    else
      v_r(i) = vmax * (rmax / r(i)) ** a
    end if
  end do
  call output_1d(v_r, "vt.txt")
  do i = 1, nr
    v_r(i) = v_r(i) * exp(-(r(i)/rcut)**6)
  end do
  call output_1d(v_r, "v_r.txt")
  do i = 1, n_smooth
    v_r(2:nr-1) = 0.25 * v_r(1:nr-2) + 0.5 * v_r(2:nr-1) + 0.25 * v_r(3:nr)
  end do
  call output_1d(v_r, "v_smooth.txt")
  ! v(方位角方向風速)の鉛直方向分布
  do i = 1, nz
    if (z(i) < zmax) then
      v_z(i) = exp(-(z(i)-zmax)**beta/(beta*lz_low**beta))
    else
      v_z(i) = exp(-(z(i)-zmax)**beta/(beta*lz_high**beta))
    end if
  end do
  call output_1d(v_z, "v_z.txt")
  ! v(r,z)の計算
  do i = 1, nr
    do k = 1, nz
      vor_v(i,k) = v_r(i) * v_z(k)
    end do
  end do
  ! p(r,z), T(r,z)の計算
  do k = 1, nz
    vor_p(:,k) = p_bs(k)
    vor_T(:,k) = T_bs(k)
  end do
  call output_2d(vor_v, "vor_v.txt")
  call hydrostatic_balance
  call output_1d(vor_rho(1,:), "bs_rho.txt")
  
  do i = 1,n_balance
    p_ = vor_p
    call gradient_balance
    call hydrostatic_balance
    p_ = p_ - vor_p
    p_ = p_ * p_
    write(11,*) sum(p_)/size(p_)
  end do
  vor_T = vor_p / (287.1 * vor_rho)

  call output_2d(vor_p, "vor_p.txt")
  call output_2d(vor_T, "vor_T.txt")
  call output_2d(vor_rho, "vor_rho.txt")
  close(11)
contains
subroutine input_1d(data,filepath)
  implicit none
  character(len=*) :: filepath
  integer :: ios
  real(8), intent(inout) :: data(nz)
  open(unit=10, iostat=ios, file=filepath, action='read', &
        & form='formatted', status='old', position='rewind')
  ! ファイルが正常に開けたかどうかをチェックする
if(ios /= 0) then
  write(11,*) 'ios: ', ios
  write(11,*) 'Failed to open file"', filepath, '"for output'
  stop
endif
read(10,*) data
write(11,*) "input", filepath
close(10)
end subroutine input_1d
subroutine output_1d(data,filename)
  implicit none
  integer, parameter :: n_char = 256
  real(8) :: data(:)
  character(len=*) filename
  character(n_char) filepath
  integer :: unit = 10
  integer :: ios
  filepath = trim(output_folderpath)//trim(filename)
  open(unit=unit, iostat=ios, file=filepath, action='write', &
        &access="stream", form='formatted',status='replace')
  ! ファイルが正常に開けたかどうかをチェックする
  if(ios /= 0) then
    write(11,*) 'ios: ', ios
    write(11, *) 'Failed to open file"', filepath, '"for input'
    stop
  endif
  write(unit,*) data
  close(unit)
  write(11,*) "output", filename
end subroutine
subroutine output_2d(data,filename)
  implicit none
  integer, parameter :: n_char = 256
  real(8) :: data(:,:)
  character(len=*) filename
  character(n_char) filepath
  integer :: unit = 10
  integer :: ios
  filepath = trim(output_folderpath)//trim(filename)
  open(unit=unit, iostat=ios, file=filepath, action='write', &
        &access="stream", form='formatted',status='replace')
  ! ファイルが正常に開けたかどうかをチェックする
  if(ios /= 0) then
    write(11,*) 'ios: ', ios
    write(11, *) 'Failed to open file"', filepath, '"for output'
    stop
  endif
  write(unit,*) data
  close(unit)
  write(11,*) "output", filename
end subroutine
subroutine hydrostatic_balance
  real(8) :: left_term
  integer :: i,k
  do i = 1, nr
    k = 1
    left_term = (vor_p(i,k+1) - vor_p(i,k)) / (z(k+1) - z(k))
    vor_rho(i,k) = - left_term / g
    do k = 2, nz-1
      left_term = (vor_p(i,k+1) - vor_p(i,k-1)) / (z(k+1) - z(k-1))
      vor_rho(i,k) = - left_term / g
    end do
    k = nz
    left_term = (vor_p(i,k) - vor_p(i,k-1)) / (z(k) - z(k-1))
    vor_rho(i,k) = - left_term / g
  end do
end subroutine hydrostatic_balance
subroutine gradient_balance
  integer :: i,k
  real(8) :: v_
  real(8) :: rho_
  real(8) :: term1
  real(8) :: term2
  real(8) :: right_term
  do i = nr, 2, -1
    do k = 1, nz
      v_ =  0.5 * (vor_v(i,k) + vor_v(i-1,k))
      rho_ = 0.5 * (vor_rho(i,k) + vor_rho(i-1,k))
      term1 = f * v_
      term2 = v_ ** 2 / r(i)
      right_term = rho_ * (term1 + term2)
      vor_p(i-1,k) = vor_p(i,k) - right_term * dr
    end do
  end do
end subroutine gradient_balance
end program vortex
