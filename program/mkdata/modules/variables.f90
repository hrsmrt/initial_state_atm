module variables
  implicit none
  real(8), allocatable :: bs_pre(:)
  real(8), allocatable :: bs_tem(:)
  real(8), allocatable :: bs_qv(:)
  real(8), allocatable :: u_profile(:)
  real(8), allocatable :: pre(:,:,:)
  real(8), allocatable :: tem(:,:,:)
  real(8), allocatable :: rho(:,:,:)
  real(8), allocatable :: qv(:,:,:)
  real(8), allocatable :: u(:,:,:)
  real(8), allocatable :: v(:,:,:)
end module variables
