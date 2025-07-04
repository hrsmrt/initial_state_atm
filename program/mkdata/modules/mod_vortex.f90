module mod_vortex
  character(len=256) :: vortex_folder
  real(4), allocatable :: r(:)
  real(4), allocatable :: z(:)
  real(4), allocatable :: v_r(:)
  real(4), allocatable :: v_z(:)
  real(4), allocatable :: p_bs(:)
  real(4), allocatable :: T_bs(:)
  real(4), allocatable :: rho_bs(:)
  real(4), allocatable :: vor_v(:,:)
  real(4), allocatable :: vor_p(:,:)
  real(4), allocatable :: vor_p_all(:,:)
  real(4), allocatable :: p_(:,:)
  real(4), allocatable :: vor_T(:,:)
  real(4), allocatable :: vor_T_all(:,:)
  real(4), allocatable :: vor_rho(:,:)
  real(4), allocatable :: vor_rho_all(:,:)
  real(4) :: vortex_size
  integer :: nr
  real(4) :: dr ! m
  real(4) :: a
  real(4) :: vmax
  real(4) :: rmax
  real(4) :: rcut
  integer :: n_smooth
  real(4) :: zmax
  real(4) :: lz
  real(4) :: lz_low
  real(4) :: lz_high
  real(4) :: beta
  integer :: n_balance
  integer :: z_calc_max
  namelist / vortex_param / &
  vortex_folder, &
  vortex_size, &
  nr, &
  a, &
  vmax, &
  rmax, &
  rcut, &
  n_smooth, &
  zmax, &
  lz_low, &
  lz_high, &
  beta, &
  n_balance, &
  z_calc_max
end module mod_vortex
