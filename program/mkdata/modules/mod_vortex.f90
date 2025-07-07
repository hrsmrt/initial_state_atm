module mod_vortex
  character(len=256) :: vortex_folder
  real(8), allocatable :: r(:)
  real(8), allocatable :: z(:)
  real(8), allocatable :: v_r(:)
  real(8), allocatable :: v_z(:)
  real(8), allocatable :: p_bs(:)
  real(8), allocatable :: T_bs(:)
  real(8), allocatable :: rho_bs(:)
  real(8), allocatable :: vor_v(:,:)
  real(8), allocatable :: vor_p(:,:)
  real(8), allocatable :: vor_p_all(:,:)
  real(8), allocatable :: p_(:,:)
  real(8), allocatable :: vor_T(:,:)
  real(8), allocatable :: vor_T_all(:,:)
  real(8), allocatable :: vor_rho(:,:)
  real(8), allocatable :: vor_rho_all(:,:)
  real(8) :: vortex_size
  integer :: nr
  real(8) :: dr ! m
  real(8) :: a
  real(8) :: vmax
  real(8) :: rmax
  real(8) :: rcut
  integer :: n_smooth
  real(8) :: zmax
  real(8) :: lz
  real(8) :: lz_low
  real(8) :: lz_high
  real(8) :: beta
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
